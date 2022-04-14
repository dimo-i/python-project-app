
from django.views import generic as views
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from progress_app.accounts.models import Profile
from progress_app.common.view_mixin import RedirectToDashboard
from progress_app.main.models import Project, Category


from rest_framework import generics as api_views
from rest_framework import serializers
"""
Try with REST
==============================================
"""
# class ProjectListSerializer(serializers.ModelSerializer):
#     project_image = serializers.ImageField(required=False)
#     class Meta:
#         model = Project
#         fields=('id', 'name', 'category', 'description', 'user')
#
#
# class ProjectsPageView(api_views.ListAPIView):
#     # queryset = Project.objects.all()
#     # serializer_class = ProjectListSerializer
#     # pagination_class = 3
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'project/projects.html'
#
#
#     def get(self, request):
#         serializer_class = [ProjectListSerializer]
#         queryset = Profile.objects.all()
#         return Response({'serializer': serializer_class, 'projects': queryset})
#
#
#
# class CategoryListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('id', 'name', 'category_image', 'category_description')
#
#
# class CategoriesPageView(api_views.ListAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategoryListSerializer
#


"""
===============================================================================
"""

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
