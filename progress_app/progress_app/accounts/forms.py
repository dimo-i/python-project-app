from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

from progress_app.accounts.models import Profile
from progress_app.common.helpers import BootstrapFormMixin


class CreateProfileForm(BootstrapFormMixin, auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,
    )
    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH
    )
    email = forms.EmailField()
    profile_picture = forms.URLField()
    gender = forms.ChoiceField(
        choices=Profile.GENDERS,
    )

    description = forms.CharField(
        widget=forms.Textarea,
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            profile_picture=self.cleaned_data['profile_picture'],
            email=self.cleaned_data['email'],
            description=self.cleaned_data['description'],
            gender=self.cleaned_data['gender'],
            user=user,
        )
        if commit:
            profile.save()
        return user

    def clean_password(self):
        if self.data['password'] != self.data['password_confirm']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password']

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'profile_picture', 'description')
        error_messages = {
            'username': {
                'unique': ("This username is already taken"),
            },
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                },
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name',
                },
            ),
            'profile_picture': forms.TextInput(
                attrs={
                    'placeholder': 'Enter URL',
                },
            )
        }

class EditProfieForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'profile_picture', 'email', 'description', 'gender')

