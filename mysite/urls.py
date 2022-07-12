from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from django.conf.urls import url
from monitorsites.views import *
from . import views
from monitorsites.views import homepage,report,check_now

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', homepage),
    path(r'^report/(?P<pk>\w+)/$', report),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),

    # Paypal forms
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('/paypal-return/', views.PaypalReturnView.as_view(), name='paypal-return'),
    path('/paypal-cancel/', views.PaypalCancelView.as_view(), name='paypal-cancel'),

    path('accounts/', include('allauth.urls')),
    path("monitorsites_check/(?P<pk>\w+)/$", check_now),
]


urlpatterns = urlpatterns + [
    # Monitor Sites
    url(r'^monitorsites_check/(?P<pk>\w+)/$', check_now),
    url(r'^monitorsites/$', MonitorSiteList.as_view(), name='montiorsites_list'),
    # Forms
    url(r'^monitorsites_add/$', MonitorSiteCreate.as_view(), name='monitorsites_add'),
    url(r'^monitorsites_update/(?P<pk>\w+)/$', MonitorSiteUpdate.as_view(), name='monitorsites_update'),
    url(r'^monitorsites_delete/(?P<pk>\w+)/$', MonitorSiteDelete.as_view(), name='monitorsites_delete'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns = urlpatterns + [
        # For anything not caught by a more specific rule above, hand over to
        # the list:
        path('__debug__/', include('debug_toolbar.urls')),
]
