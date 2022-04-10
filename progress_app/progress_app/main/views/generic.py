
from django.shortcuts import redirect
from django.views import generic as views

from progress_app.accounts.models import Profile
from progress_app.common.view_mixin import RedirectToDashboard
from progress_app.main.models import Project, Category


class HomePageView(RedirectToDashboard, views.TemplateView):
    template_name = 'main/home_page_non_auth.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_additional_nav_items'] = True
        return context



class DashboardPageView(views.TemplateView):
    template_name = 'main/dashboard.html'



class ProjectsPageView(views.ListView):
    model = Project
    template_name = 'project/projects.html'
    context_object_name = 'projects'
    paginate_by = 3




class CategoriesPageView(views.ListView):
    model = Category
    template_name = 'category/categories.html'
    context_object_name = 'categories'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.object_list

        return context



class ProjectsByCategoriesPageView(views.ListView):
    model = Project
    template_name = 'project/projects.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        category_name = Category.objects.get(id=pk)
        context['category'] = category_name
        context['projects'] = self.object_list.filter(category_id=pk)
        return context


class ProjectsByProfilesPageView(views.ListView):
    model = Project
    template_name = 'project/projects.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['profile'] = Profile.objects.get(user=pk).user
        context['projects'] = Project.objects.filter(user_id=pk)
        return context
