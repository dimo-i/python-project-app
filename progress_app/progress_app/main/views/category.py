from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixin

from progress_app.common.helpers import SuperUserCheck
from progress_app.main.views.forms import CreateCategoryForm

#required login / super user required



# @staff_member_required
class CreateCategoryView(auth_mixin.LoginRequiredMixin, SuperUserCheck,views.CreateView):
    template_name = 'category/create_category.html'
    form_class = CreateCategoryForm
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs