from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages

from django.http import HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import View
from django.shortcuts import redirect

from .models import MonitorSite, Status

from .forms import MonitorSiteForm

def homepage(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'home_page.html')

def report(request):
    """View function for report page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'report.html')

class MonitorSiteList(ListView):
    """
    Monitored Sites
    """
    model = MonitorSite
    template_name = 'monitorsite_list.html'

    def get(self, request, *args, **kwargs):

        getSites = MonitorSite.objects.all()

        return render(request, self.template_name, {'getSites': getSites,})

class MonitorSiteCreate(CreateView):
    """
    Montior for sites creation
    """
    model = MonitorSite
    template_name = 'monitorsite_form.html'
    #pre-populate parts of the form
    def get_initial(self):
        initial = {
            'user': self.request.user,
            }

        return initial

    def get_form_kwargs(self):
        kwargs = super(MonitorSiteCreate, self).get_form_kwargs()
        kwargs["action_name"] = "monitorsites_add"
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Monitored Site Created!')
        return redirect('/monitorsites/')

    form_class = MonitorSiteForm


class MonitorSiteUpdate(UpdateView):
    """
    Update and Edit Montiored Site.
    """
    model = MonitorSite
    template_name = 'monitorsite_form.html'
    fields = ['name','url','polling_interval','description','status']
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return render(self.get_context_data(form=form))

    def form_valid(self, form):
        site = MonitorSite.objects.get(pk=self.kwargs.get('pk'))
        self.object = form.save()

        messages.success(self.request, 'Success, Monitored Site Updated!')

        return redirect('/monitorsites/')


class MonitorSiteDelete(DeleteView):
    """
    Delete a MontiorSite
    """
    model = MonitorSite

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return render(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()
        messages.success(self.request, 'Success, Montior Site Deleted!')
        return redirect('/monitorsites/')
