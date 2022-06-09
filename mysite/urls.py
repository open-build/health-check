from django.conf import settings
from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path('django-admin/', admin.site.urls),
]

from django.conf.urls import url
from monitorsites import views as homeviews

urlpatterns = [

    # Monitor Sites
    url(r'^monitorsites/(?P<pk>\w+)/$', MonitorSiteList.as_view(), name='montiorsites_list'),
    # Forms
    url(r'^monitorsites_add/(?P<id>\w+)/$', MonitorSiteCreate.as_view(), name='monitorsites_add'),
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
        # Wagtail's page serving mechanism. This should be the last pattern in
        # the list:
        path('__debug__/', include('debug_toolbar.urls')),
        # Alternatively, if you want Wagtail pages to be served from a subpath
        # of your site, rather than the site root:
        #    path("pages/", include(wagtail_urls)),
]
