from django.contrib.auth import mixins as auth_mixin, get_user_model

from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views, login

from progress_app.accounts.forms import CreateProfileForm, EditProfieForm
from progress_app.accounts.models import Profile
from progress_app.common.helpers import SuperUserCheck
from progress_app.main.models import Project



class RegisterUserPageView(views.CreateView):
    form_class = CreateProfileForm
    template_name = 'accounts/register_user.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class LoginUserPageView(auth_views.LoginView):
    template_name = 'accounts/login_user.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class LogoutUserPageView(auth_mixin.LoginRequiredMixin, auth_views.LogoutView):
    template_name = 'accounts/logout_user.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()



#auth_mixin.PermissionRequiredMixin
#Permission for presentation?
class ProfileDetailsPageView(auth_mixin.LoginRequiredMixin, views.DetailView):
    model = Profile
    template_name = 'accounts/user_details.html'
    context_object_name = 'profile'
    # permission_required = ('accounts.view_profile',)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_projects = list(Project.objects.filter(user_id=self.object.user_id))
        total_projects_count = len(all_projects)
        context.update({
            'total_projects_count': total_projects_count,
            'is_owner': self.object.user_id == self.request.user.id,
            'all_projects': all_projects,
        })
        return context

#auth_mixin.PermissionRequiredMixin
#Permission for presentation?
class EditProfilePageView(auth_mixin.LoginRequiredMixin, views.UpdateView):
    model = Profile
    template_name = 'accounts/user_edit.html'
    form_class = EditProfieForm
    # permission_required = ('accounts.can_change_profile',)

    def form_valid(self, form):
        result = super().form_valid(form)
        return result

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('user details', kwargs={'pk': pk})



#Only of admins/staff users
class ShowAllProfilesPageView(auth_mixin.LoginRequiredMixin, SuperUserCheck, views.ListView):
    model = Profile
    template_name = 'main/admin_all_profiles.html'
    context_object_name = 'profiles'
    paginate_by = 3



class ChangePasswordPageView(auth_mixin.LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'accounts/user_change_pwd.html'
    success_url=reverse_lazy('dashboard')



# To avoid DataBase errors, only admin/permitted users will delete accounts(deactivate users/profiles) +related projects
class DeleteProfilePageView(auth_mixin.LoginRequiredMixin, auth_mixin.PermissionRequiredMixin, views.DeleteView):
    model = get_user_model()
    template_name = 'accounts/delete_user.html'
    permission_required = ('accounts.can_delete_profile',)
    success_url = reverse_lazy('dashboard')
    context_object_name = 'profile'

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()
