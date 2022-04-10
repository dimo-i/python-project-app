from django.contrib import admin

# Register your models here.

from progress_app.accounts.models import Profile, ProgressAppUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


@admin.register(ProgressAppUser)
class ProgressAppUserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)