
from django.urls import reverse_lazy
from django.views import generic as views

from django.contrib.auth import mixins as auth_mixin

from progress_app.accounts.models import Profile
from progress_app.main.models import Project, ProjectAlbum
from progress_app.main.views.forms import CreateProjectForm, CreateAlbumForm, EditProjectForm


class CreateProjectView(auth_mixin.LoginRequiredMixin, views.CreateView):
    template_name = 'project/create_project.html'
    form_class = CreateProjectForm
    success_url = reverse_lazy('dashboard')


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class ProjectDetailsView(views.DetailView):
    model = Project
    template_name = 'project/project_details_page.html'
    context_object_name = 'project'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user_id == self.request.user.id
        context['album'] = ProjectAlbum.objects.filter(project_id=self.object.id)
        context['user'] = Profile.objects.get(user_id=self.object.user_id).user
        return context




class EditProjectView(auth_mixin.LoginRequiredMixin, views.UpdateView):
    model = Project
    template_name = 'project/edit_project.html'
    # context_object_name = 'project'
    form_class = EditProjectForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('project details', kwargs={'pk': pk})


#TODO
class DeleteProjectView(auth_mixin.LoginRequiredMixin, views.DeleteView):
    model = Project
    template_name = 'project/delete_project.html'
    # form_class = DeleteProjectForm -
    # context_object_name = 'project'


    def get_success_url(self):
        return reverse_lazy('dashboard')




#TODO - album not visible when anonymous
class ProjectAlbumView(auth_mixin.LoginRequiredMixin , views.ListView):
    model = ProjectAlbum
    template_name = 'album/album_page.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['project_id'] = pk
        context['album'] = ProjectAlbum.objects.filter(project_id=pk)
        current_project_owner = Project.objects.get(id=pk).user_id
        context['is_owner'] = current_project_owner==self.request.user.id
        return context


class AddImageToAlbumView(auth_mixin.LoginRequiredMixin, views.CreateView):
    template_name = 'album/add_album_image.html'
    form_class = CreateAlbumForm

    def form_valid(self, form):
        form.instance.project_id = self.kwargs['pk']
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['project_id'] = pk

        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('project album', kwargs={'pk': pk})

#TODO delete ALbumImage/Album?