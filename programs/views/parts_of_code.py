
# Django
from django.views.generic import ListView, DetailView, FormView, View
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect, Http404

# Mixins
from psp.mixins import MemberUserProgramRequiredMixin

# Models
from programs.models import Program, BasePart, ReusedPart, NewPart

# Models 
from programs.forms import CreateBasePartForm

    

class CreatePartProgramView(MemberUserProgramRequiredMixin, FormView):
    template_name = 'parts_of_code/parts.html'

    def get_form_class(self):
        self.type_part = self.request.GET['type_part']
        if self.type_part and (self.type_part == 'base' or self.type_part == 'reused' or self.type_part == 'new'):
            if self.type_part == 'base':
                return CreateBasePartForm
        else:
            raise Http404("The URL doesn't valid")
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["program_opened"] = self.program
        context["base_programs"] = Program.objects.exclude(pk=self.program.pk).filter(programmer=self.request.user)

        context["base_parts"] = BasePart.objects.filter(program=self.program)
        context["reused_parts"] = ReusedPart.objects.filter(program=self.program)
        context["new_parts"] = NewPart.objects.filter(program=self.program)

        return context
    

    def form_valid(self, form):
        form.save(self.program)
        self.request.session['part_created'] = "The {} part was created successfully".format(self.type_part)
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('programs:create_part_program', kwargs={'pk_program': self.program.pk}) + "?type_part={}".format(self.type_part)
