from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import View
from django.shortcuts import redirect

from .health_check import check_now as check_site

from .models import MonitorSite, MonitorSiteEntry
from .forms import MonitorSiteForm
import requests

class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

def homepage(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'home_page.html')

@login_required(login_url='/')
def report(request,pk):
    """View function for report page of site."""
    model = MonitorSiteEntry

    def get(self, request, *args, **kwargs):

        getReport = MonitorSiteEntry.objects.get(site__id=pk)

        url = 'https://api.wappalyzer.com/lookup/v2/?urls=' + getReport.url + '&sets=email,phone,contact,social,meta,locale'
        headers = {'x-api-key' : 'ufskVhLffl7keYV7UsHTm14GJH4NQgeAa72kdd4C'}
        r = requests.get(url, headers=headers)
        analysis = r.json()

        return render(request, self.template_name, {'getReport': getReport, 'wapp': analysis })
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'report.html')

@login_required(login_url='/')
def check_now(request,pk):
    """Check the status of a site."""
    message = check_site(pk)
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'health_check.html',{'message': message,})

class MonitorSiteList(ListView,LoginRequiredMixin):
    """
    Monitored Sites
    """
    model = MonitorSite
    template_name = 'monitorsite_list.html'

    def get(self, request, *args, **kwargs):

        getSites = MonitorSite.objects.all().filter(owner=request.user)

        return render(request, self.template_name, {'getSites': getSites,})

class MonitorSiteCreate(CreateView,LoginRequiredMixin,):
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
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.url = form.instance.url.replace("http://","")
        form.instance.url = form.instance.url.replace("https://","")
        form.save()
        messages.success(self.request, 'Success, Monitored Site Created!')
        return redirect('/monitorsites/')

    form_class = MonitorSiteForm


class MonitorSiteUpdate(UpdateView,LoginRequiredMixin,):
    """
    Update and Edit Montiored Site.
    """
    model = MonitorSite
    template_name = 'monitorsite_form.html'
    form_class = MonitorSiteForm

    def get_form_kwargs(self):
        kwargs = super(MonitorSiteUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return render(self.get_context_data(form=form))

    def form_valid(self, form):
        form.instance.url = form.instance.url.replace("http://","")
        form.instance.url = form.instance.url.replace("https://","")
        form.save()
        messages.success(self.request, 'Success, Monitored Site Updated!')

        return redirect('/monitorsites/')


class MonitorSiteDelete(DeleteView,LoginRequiredMixin,):
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
