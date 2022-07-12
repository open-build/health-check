from datetime import timedelta
from decimal import Decimal
import uuid

from django.db import models
from django.contrib import admin
from django.utils import timezone


class MonitorSite(models.Model):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey('auth.User',blank=True, null=True, on_delete=models.CASCADE)
    url = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, blank=True)
    ssl_expirtaion = models.DateTimeField(null=True, blank=True)
    ssl_status = models.CharField(max_length=255, blank=True)
    last_polled_date_time = models.DateTimeField(null=True, blank=True)
    polling_interval = models.IntegerField(default=0, blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(MonitorSite, self).save(*args, **kwargs)


class MonitorSiteAdmin(admin.ModelAdmin):
    list_display = ('name','owner','url','status','create_date','edit_date')
    search_fields = ('name','owner','status')
    list_filter = ('name',)
    display = 'Montior Sites'


class MonitorSiteEntry(models.Model):
    site = models.ForeignKey(MonitorSite, null=False, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, blank=True)
    url_message = models.CharField(max_length=255, blank=True)
    ssl_expirtaion = models.DateTimeField(null=True, blank=True)
    ssl_status = models.CharField(max_length=255, blank=True)
    ssl_message = models.CharField(max_length=255, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(MonitorSiteEntry, self).save(*args, **kwargs)


class MonitorSiteEntryAdmin(admin.ModelAdmin):
    list_display = ('site','status','create_date','edit_date')
    search_fields = ('site__name','status')
    list_filter = ('site__name','status')
    display = 'Montior Site Entries'


class Plan(models.Model):
    site = models.ForeignKey(MonitorSite, null=False, on_delete=models.CASCADE)
    is_paid = models.Boolean(default=False)
    plan = models.CharField(max_length=255, blank=True)
    expriation_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Plan, self).save(*args, **kwargs)


class PlanAdmin(admin.ModelAdmin):
    list_display = ('site','is_paid','plan','create_date','edit_date')
    search_fields = ('site__name','is_paid')
    list_filter = ('site__name','is_paid')
    display = 'Payment Plans'
