from .models import *
from django.contrib import admin

admin.site.register(MonitorSite, MonitorSiteAdmin)
admin.site.register(MonitorSiteEntry, MonitorSiteEntryAdmin)
