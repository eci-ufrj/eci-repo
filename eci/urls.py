from django.conf.urls.defaults import *
from django.contrib import admin
from eci import settings
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$','views.home',{'template_name':'hello.html'},'home'),
    url(r'^$',direct_to_template,{'template':'home.html'},'home'),
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$','django.views.static.serve',
     { 'document_root' : settings.MEDIA_ROOT}),
    (r'^users/', include('registration.backends.default.urls')),
    (r'^resources/',include('resources.urls')),
    (r'^results/$','resources.views.results',{'template_name':'resources/results.html'}, 'search_results'),
    (r'^profiles/', include('profiles.urls')),
    (r'^help/',direct_to_template,{'template':'help.html'}),
    (r'^statistics/','views.statistics',{'template_name':'statistics.html'},'statistics'),

)
