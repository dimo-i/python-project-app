from datetime import date

from django import test as django_test

# Create your tests here.
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse

from progress_app.accounts.models import Profile
from progress_app.accounts.views import ShowAllProfilesPageView
from progress_app.main.models import Project, Category, ProjectAlbum

UserModel = get_user_model()


class ProfileDetailsPageViewTest(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'TestUser',
        'password': '123456qwer',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'First NameTest',
        'last_name': 'Last NameTest',
        'profile_picture': 'http://test.picture.com/test.jpg',
        'gender': 'Male',
    }

    VALID_CATEGORY_DATA = {
        'name': 'Test Category',
        'category_description': 'Test Description',
        'category_image': 'http://test.picture.com/test.jpg',
    }


    VALID_PROJECT_DATA = {
        'name': 'TestProject',
        'project_image': 'http://test.picture.com/test.jpg',
        'post_date': date.today()
    }

    VALID_PROJECT_ALBUM_IMAGE_DATA = {
        'album_image': 'http://test.picture.com/test.jpg',
        'image_description': 'TEST Description',
    }

    def __create_valid_category(self):
        category = Category.objects.create(
            **self.VALID_CATEGORY_DATA
        )
        return category


    def __create_valid_project_album(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        category = self.__create_valid_category()
        project = Project.objects.create(
            **self.VALID_PROJECT_DATA
        )
        album = ProjectAlbum.objects.create(
            **self.VALID_PROJECT_ALBUM_IMAGE_DATA,
            user=user,
            category=category,
            project=project,
        )
        return album


    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        return (user, profile)


    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __get_response_for_profile(self, profile):
        return self.client.get(reverse('user details', kwargs={'pk': profile.pk}))


    def test_when_opening_not_existing_profile__expect_404(self):
        response = self.client.get(reverse('user details', kwargs={
            'pk': 1,
        }))
        self.assertTemplateUsed('404.html')

    def test_expect_correct_template(self):
        user, profile = self.__create_valid_user_and_profile()
        self.__get_response_for_profile(profile)
        self.assertTemplateUsed('accounts/user_details.html')

    def test_if_user_is_owner__expect_to_be_true(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile(profile)
        self.assertTrue(response.context['is_owner'])

    def test_if_user_is_not_owner__expect_to_be_false(self):
        _, profile = self.__create_valid_user_and_profile()
        credentials = {
            'username': 'testuser2',
            'password': '123123123',
        }
        self.__create_user(**credentials)
        self.client.login(**credentials)
        response = self.__get_response_for_profile(profile)

        self.assertFalse(response.context['is_owner'])


    def test_if_user_have_projects__expect_to_have_one(self):
        user, profile = self.__create_valid_user_and_profile()
        category = self.__create_valid_category()
        project = Project.objects.create(
            **self.VALID_PROJECT_DATA,
            category=category,
            user=user,
        )
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile(profile)

        self.assertEqual(1, response.context['total_projects_count'])


    def test_if_user_dont_have_projects__expect_to_be_none(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile(profile)

        self.assertEqual(0, response.context['total_projects_count'])

    #TODO
    # def test_register_user_with_same_username__raise_error(self):
    #     user, profile = self.__create_valid_user_and_profile()
    #     user2, profile2 = self.__create_valid_user_and_profile()
    #
    #     self.assertRaises(, "This username is already taken")

    def test_if_user_can_see_all_profiles_if_not_superuser__expect_to_be_403(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('all users'))
        self.assertEqual(response.status_code, 403)

    def test_register_user_with_invalid_data(self):
        pass

    def test_change_user_details(self):
        pass