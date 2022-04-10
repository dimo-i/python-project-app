from django.contrib import admin

# Register your models here.
from progress_app.main.models import Category, Project, ProjectAlbum


class CategoryInLineAdmin(admin.StackedInline):
    model = Category

class ProjectImageAdmin(admin.StackedInline):
    model = ProjectAlbum



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [ProjectImageAdmin]

    class Meta:
        model = Project


@admin.register(ProjectAlbum)
class ProjectImageAdmin(admin.ModelAdmin):
    pass
