from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from ideahub import settings


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('ideahub.apps.home.urls')),
    url(r'^accounts/', include('ideahub.apps.accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('ideahub.apps.api.urls', namespace='api')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
urlpatterns += staticfiles_urlpatterns()


