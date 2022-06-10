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

from .models import MonitorSite, Status

from .forms import MonitorSiteForm

def homepage(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'home_page.html')

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
    template_name = 'monitor_form.html'

    #pre-populate parts of the form
    def get_initial(self):
        initial = {
            'user': self.request.user,
            }

        return initial

    # send prepoluated data to the form
    def get_context_data(self, **kwargs):
        context = super(MontiorSiteCreate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['id']})
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(MontiorSiteCreate, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return render(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Monitored Site Created!')
        form = ""
        return render(self.get_context_data(form=form))

    form_class = MonitorSiteForm


class MonitorSiteUpdate(UpdateView):
    """
    Update and Edit Montiored Site.
    """

    def get_template_names(self):
        return 'monitor_form.html'

    def dispatch(self, request, *args, **kwargs):
        return super(MontiorSiteUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MontiorSiteUpdate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        getIndicator = MontiorSite.objects.get(id=self.kwargs['pk'])

        return context

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(MontiorSiteUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        site = MontiorSite.objects.all().filter(id=self.kwargs['pk'])
        kwargs['site'] = site
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return render(self.get_context_data(form=form))

    def form_valid(self, form):
        site = MontiorSite.objects.get(pk=self.kwargs.get('pk'))
        self.object = form.save()

        messages.success(self.request, 'Success, Monitored Site Updated!')

        return render(self.get_context_data(form=form))


class MonitorSiteDelete(DeleteView):
    """
    Delete a MontiorSite
    """
    success_url = '/monitor_site/'

    def dispatch(self, request, *args, **kwargs):
        return super(MontiorSiteDelete, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return render(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Montior Site Deleted!')
        return render(self.get_context_data(form=form))
