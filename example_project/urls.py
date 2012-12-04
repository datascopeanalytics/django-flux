from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^', include('flux.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^%s(?P<path>.*)$'%settings.MEDIA_URL, 
            'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
