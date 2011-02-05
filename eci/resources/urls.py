from django.conf.urls.defaults import *
from models import Resource,Subject,Professor
urlpatterns = patterns('eci.resources.views',
                       (r'^subject/(?P<subject_slug>[-\w]+)/$','show_subject',{ 'template_name': 'resources/subject.html'},'resources_subject'),
                       (r'^professor/(?P<professor_slug>[-\w]+)/$','show_professor',{ 'template_name': 'resources/professor.html'},'resources_professor'),
                       (r'^resource/(?P<resource_slug>[-\w]+)/$','show_resource',{ 'template_name': 'resources/resource.html'},'resources_resource'),
                       (r'^subjects/$','show_subjects',{ 'template_name': 'resources/subjects.html'},'resources_subjects'),
                       (r'^professors/$','show_professors',{ 'template_name': 'resources/professors.html'},'resources_professors'),
                       (r'^add_resource/$','add_resource',{ 'template_name': 'resources/resource_form.html'},'resources_add_resource'),
                       (r'^add_resource_rating/$','add_rating',{'object':Resource},'resources_add_rating'),
                       (r'^add_subject_rating/$','add_rating',{'object':Subject},'resources_add_rating'),
                       (r'^add_professor_rating/$','add_rating',{'object':Professor},'resources_add_rating'),
                       (r'^add_resource_professor/$','add_resource_professor',{},'resources_add_resource_professor'),
                       (r'^add_professor/$','add_professor',{},'resources_add_professor'),
                       (r'^check_professor/$','check_professor',{},'resources_check_professor'),
                       (r'^download/(?P<resource_slug>[-\w]+)/$','download',{},'resources_download'),
                       
                       )