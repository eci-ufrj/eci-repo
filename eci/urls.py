from django.conf.urls.defaults import *
from django.contrib import admin
from eci import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','views.home',{'template_name':'hello.html'},'home'),
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$','django.views.static.serve',
     { 'document_root' : settings.MEDIA_ROOT}),
    (r'^users/', include('registration.backends.default.urls')),
    (r'^resources/',include('resources.urls')),
    (r'^results/$','resources.views.results',{'template_name':'resources/results.html'}, 'search_results'),
    (r'^profiles/', include('profiles.urls')),


)
