from django import forms

from progress_app.common.helpers import BootstrapFormMixin
from progress_app.main.models import Project, Category, ProjectAlbum


class CreateProjectForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        project = super().save(commit=False)
        project.user = self.user
        if commit:
            project.save()
        return project

    class Meta:
        model = Project
        fields = ('name', 'description', 'project_image', 'category',)


class EditProjectForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        project = super().save(commit=False)
        project.user = self.user
        if commit:
            project.save()
        return project

    class Meta:
        model = Project
        fields = ('name', 'description', 'project_image', 'category',)


#Current logic deletes the project without form?!?!
# class DeleteProjectForm(BootstrapFormMixin, DisabledFieldsFormMixin, forms.ModelForm):
#
#     def save(self, commit=True):
#         Project.objects.filter(id=id)
#         return self.instance
#
#     class Meta:
#         model = Project
#         fields = ('name', 'description', 'image', 'category',)



class CreateCategoryForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        category = super().save(commit=False)

        if commit:
            category.save()
        return category

    class Meta:
        model = Category
        fields = ('name', 'category_description', 'category_image', )

class CreateAlbumForm(BootstrapFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def save(self,commit=True):
        album = super().save(commit=False)

        if commit:
            album.save()
        return album

    class Meta:
        model = ProjectAlbum
        fields = ('album_image', 'image_description')



