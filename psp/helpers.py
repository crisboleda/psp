
# Django
from django.views.generic import FormView, View


class FormViewDefaultValue(FormView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.set_values_init_form(context["form"])
        return context

    def set_values_init_form(self, form):
        pass