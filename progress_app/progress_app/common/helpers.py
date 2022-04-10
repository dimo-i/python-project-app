from django import forms
from django.contrib.auth import mixins as auth_mixin
from django.views import generic as views

class BootstrapFormMixin:
    fields = {}
    def _init_bootstrap_form_controls(self):
        for _, field in self.fields.items():
            if hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += ' form-control'


#TODO to be checked///
class DisabledFieldsFormMixin:
    disabled_fields = '__all__'
    fields = {}
    def _init_disabled_fields(self):
        for name, field in self.fields.items():
            if self.disabled_fields != '__all__' and name not in self.disabled_fields:
                continue
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            if isinstance(field, forms.ChoiceField):
                field.widget.attrs['disabled'] = 'disabled'
            else:
                field.widget.attrs['readonly'] = 'readonly'



class SuperUserCheck(auth_mixin.UserPassesTestMixin, views.View):
    def test_func(self):
        return self.request.user.is_superuser

