from django.urls import path

from progress_app.main.views.category import CreateCategoryView
from progress_app.main.views.project import CreateProjectView, EditProjectView, ProjectDetailsView, DeleteProjectView, \
    ProjectAlbumView, AddImageToAlbumView, DeleteAlbumImageView
from progress_app.main.views.generic import HomePageView, DashboardPageView, ProjectsPageView, CategoriesPageView, \
    ProjectsByCategoriesPageView, ProjectsByProfilesPageView

urlpatterns = (
    path('', HomePageView.as_view(), name='index'),
    path('category/', CategoriesPageView.as_view(), name='categories'),
    path('category/create/', CreateCategoryView.as_view(), name='create category'), # only for admin
    path('category/projects_cat/<int:pk>/', ProjectsByCategoriesPageView.as_view(), name='category projects'),
    path('category/projects_prfl/<int:pk>/', ProjectsByProfilesPageView.as_view(), name='profile projects'),

    #path('category/delete/<int:pk>/') - only for admin

    path('dashboard/', DashboardPageView.as_view(), name='dashboard'),

    path('project/', ProjectsPageView.as_view(), name='projects'),
    path('project/create/', CreateProjectView.as_view(), name='create project'),

    path('project/edit/<int:pk>/', EditProjectView.as_view(),name='edit project'),
    path('project/delete/<int:pk>/', DeleteProjectView.as_view(), name='delete project'),

    path('project/details/<int:pk>/', ProjectDetailsView.as_view() ,name = 'project details'),

    path('project/album/<int:pk>/', ProjectAlbumView.as_view(), name='project album'),

    path('project/album/image/add/<int:pk>/', AddImageToAlbumView.as_view(), name='add album image'),

    path('project/album/image/delete/<int:pk>/', DeleteAlbumImageView.as_view(), name='delete album image'),






)