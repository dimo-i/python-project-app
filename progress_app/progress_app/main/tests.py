from datetime import date

from django import test as django_test
# Create your tests here.

#Views Tests
from django.contrib.auth.models import AnonymousUser

from django.urls import reverse

from progress_app.accounts.models import Profile
from progress_app.main.models import UserModel, Category, ProjectAlbum, Project
from progress_app.main.views.category import CreateCategoryView
from progress_app.main.views.project import CreateProjectView


class ViewsTests(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'TestUser',
        'password': '123456qwer'
    }
    VALID_USER2_CREDENTIALS = {
        'username': 'TestUser2',
        'password': '123456qwer22'
    }

    VALID_PROFILE_DATA = {
        'first_name': 'First NameTest',
        'last_name': 'Last NameTest',
        'profile_picture': 'http://test.picture.com/test.jpg',
        'gender': 'Male',
    }
    VALID_PROFILE2_DATA = {
        'first_name': 'First NameTest2',
        'last_name': 'Last NameTest2',
        'profile_picture': 'http://test.picture.com/test2.jpg',
        'gender': 'Male',
    }

    VALID_CATEGORY_DATA = {
        'name': 'Test Category',
        'category_description': 'Test Description',
        'category_image': 'http://test.picture.com/test.jpg',
    }
    VALID_CATEGORY2_DATA = {
        'name': 'Test Category2',
        'category_description': 'Test Description2',
        'category_image': 'http://test.picture.com/test2.jpg',
    }

    VALID_PROJECT_DATA = {
        'name': 'TestProject',
        'project_image': 'http://test.picture.com/test.jpg',
        'post_date': date.today()
    }
    VALID_PROJECT2_DATA = {
        'name': 'TestProject2',
        'project_image': 'http://test.picture.com/test2.jpg',
        'post_date': date.today()
    }

    VALID_PROJECT_ALBUM_IMAGE_DATA = {
        'album_image': 'http://test.picture.com/test.jpg',
        'image_description': 'TEST Description',
    }
    VALID_PROJECT_ALBUM_IMAGE2_DATA = {
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



    def test_project_page_view_if_no_projects__expect_to_be_none(self):
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('projects'))
        projects_count = len(response.context['projects'])
        self.assertEqual(0, projects_count)


    def test_project_page_view_if_projects__expect_to_be_true(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        category = self.__create_valid_category()
        project = Project.objects.create(
            **self.VALID_PROJECT_DATA,
            category=category,
            user=user,
        )
        project2 = Project.objects.create(
            **self.VALID_PROJECT2_DATA,
            category=category,
            user=user,
        )

        response = self.client.get(reverse('projects'))
        projects_count = len(response.context['projects'])
        self.assertEqual(2, projects_count)


    def test_category_page_view_if_no_categories__expect_to_be_false(self):
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('categories'))
        categories_count = len(response.context['categories'])
        self.assertEqual(0, categories_count)


    def test_category_page_view_if_categories__expect_to_be_true(self):
        category = self.__create_valid_category()
        category2 = Category.objects.create(
            **self.VALID_CATEGORY2_DATA
        )
        response = self.client.get(reverse('categories'))
        categories_count = len(response.context['categories'])
        self.assertEqual(2, categories_count)


    def test_correct_template_for_project(self):
        user, profile = self.__create_valid_user_and_profile()
        # self.client.login(**self.VALID_USER_CREDENTIALS)
        category = self.__create_valid_category()
        project = Project.objects.create(
            **self.VALID_PROJECT_DATA,
            category=category,
            user=user,
        )
        self.client.get(reverse('project details', kwargs={'pk': project.pk}))

        self.assertTemplateUsed('project/project_details_page.html')


    def test_if_anonymous_user_can_view_create_project_page__expect_redirect(self):
        response = self.client.get(reverse('create project'))

        self.assertRedirects(response, '/accounts/login/?next=/project/create/', status_code=302,
                            target_status_code=200, fetch_redirect_response=True)

    def test_if_anonymous_user_can_view_create_category_page__expect_redirect(self):
        response = self.client.get(reverse('create category'))

        self.assertRedirects(response, '/accounts/login/?next=/category/create/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)




    def test_if_project_does_not_exists__expect_404(self):
        response = self.client.get(reverse('project details', kwargs={
            'pk': 1,
        }))

        self.assertTemplateUsed('404.html')



    def test_if_project_exists__expect_to_be_true(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        category = self.__create_valid_category()
        project = Project.objects.create(
            **self.VALID_PROJECT_DATA,
            category=category,
            user=user,
        )
        response = self.client.get(reverse('project details', kwargs={
            'pk': 1,
        }))
        self.assertTemplateUsed('project/project_details_page.html')



    def test_if_normal_user_can_view_create_category_page__expect_to_be_false(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('create category'))
        self.assertEquals(response.status_code, 403)


    def test_project_details_view_page_is_owner__expect_to_be_true(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        category = self.__create_valid_category()
        project = Project.objects.create(
            **self.VALID_PROJECT_DATA,
            category=category,
            user=user,
        )
        response = self.client.get(reverse('project details', kwargs={
            'pk': project.pk,
        }))

        self.assertTrue(response.context['is_owner'])


    def test_project_details_view_page_is_not_owner__expect_to_be_false(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        category = self.__create_valid_category()
        project = Project.objects.create(
            **self.VALID_PROJECT_DATA,
            category=category,
            user=user,
        )
        user2 = UserModel.objects.create_user(**self.VALID_USER2_CREDENTIALS)
        profile2 = Profile.objects.create(
            **self.VALID_PROFILE2_DATA,
            user=user2,
        )
        project2 = Project.objects.create(
            **self.VALID_PROJECT2_DATA,
            category=category,
            user=user2,
        )
        response = self.client.get(reverse('project details', kwargs={
            'pk': project2.pk,
        }))
        self.assertFalse(response.context['is_owner'])



    def test_project_details_page_if_have_album__expect_to_be_true(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        category = self.__create_valid_category()
        project = Project.objects.create(
            **self.VALID_PROJECT_DATA,
            category=category,
            user=user,
        )

        album = ProjectAlbum.objects.create(
            **self.VALID_PROJECT_ALBUM_IMAGE_DATA,
            user=user,
            project=project,
        )

        response = self.client.get(reverse('project details', kwargs={
            'pk': project.pk,
        }))

        self.assertTrue(response.context['album'])



    def test_project_details_page_if_no_album__expect_to_be_false(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        category = self.__create_valid_category()
        project = Project.objects.create(
            **self.VALID_PROJECT_DATA,
            category=category,
            user=user,
        )

        response = self.client.get(reverse('project details', kwargs={
            'pk': project.pk,
        }))

        self.assertFalse(response.context['album'])


    def test_album_view_page__expect_to_be_2(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        category = self.__create_valid_category()
        project = Project.objects.create(
            **self.VALID_PROJECT_DATA,
            category=category,
            user=user,
        )
        album = ProjectAlbum.objects.create(
            **self.VALID_PROJECT_ALBUM_IMAGE_DATA,
            user=user,
            project=project,
        )
        album2 = ProjectAlbum.objects.create(
            **self.VALID_PROJECT_ALBUM_IMAGE2_DATA,
            user=user,
            project=project,
        )

        response = self.client.get(reverse('project album', kwargs={
            'pk': project.pk,
        }))

        album = len(response.context['album'])
        self.assertEqual(2, album)


    def test_create_project_with_invalid_data(self):
        pass


    def test_change_project_details(self):
        pass


