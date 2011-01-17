from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Count
from eci.resources.models import Subject

def home(request,template_name='hello.html'):
    subjects = Subject.objects.annotate(count=Count('resource')).order_by('-count')[:5]
    return render_to_response(template_name,locals(),context_instance=RequestContext(request))