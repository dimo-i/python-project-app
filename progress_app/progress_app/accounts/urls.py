from django.urls import path, reverse_lazy

from progress_app.accounts.views import LoginUserPageView, RegisterUserPageView, ProfileDetailsPageView, \
    LogoutUserPageView, EditProfilePageView, DeleteProfilePageView,  ShowAllProfilesPageView, ChangePasswordPageView

urlpatterns = (
    path('login/', LoginUserPageView.as_view(), name='login user'),
    path('logout/', LogoutUserPageView.as_view(), name='logout user'),
    path('register/', RegisterUserPageView.as_view(), name='register user'),

    path('change_password/', ChangePasswordPageView.as_view(), name='change password'),

    path('<int:pk>/', ProfileDetailsPageView.as_view(), name='user details'),
    path('edit/<int:pk>/', EditProfilePageView.as_view(), name='edit user'),
    path('delete/<int:pk>/', DeleteProfilePageView.as_view(), name='delete user'),

    path('all_profiles/', ShowAllProfilesPageView.as_view(), name='all users')

)