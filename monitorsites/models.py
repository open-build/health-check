from datetime import timedelta
from decimal import Decimal
import uuid

from django.db import models
from django.contrib import admin
from django.utils import timezone


class Status(models.Model):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Status, self).save(*args, **kwargs)


class StatusAdmin(admin.ModelAdmin):
    list_display = ('name','description','create_date','edit_date')
    search_fields = ('name',)
    list_filter = ('name',)
    display = 'Status'


class MonitorSite(models.Model):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey('auth.User',blank=True, null=True, on_delete=models.CASCADE)
    url = models.CharField(max_length=255, blank=True)
    status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.CASCADE)
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
