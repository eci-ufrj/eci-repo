# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404,render_to_response
from eci.resources.models import *
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.db.models import Q
from eci.resources import utils
from django.core.paginator import Paginator,InvalidPage, EmptyPage
from eci import settings
from eci.resources.forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson
from django.template.loader import render_to_string
from django.core.servers.basehttp import FileWrapper
from django import forms
from django.http import Http404
import os, tempfile, zipfile
import StringIO
import codecs

@login_required
def show_subject(request,subject_slug,template_name="resources/subject.html"):
    """Show the target Subject
    @in: 
    template_name: the template (if not the default)
    subject_slug: identifies the subject
    request: current request object
    
    Context Variables{}:
    subject: Target Subject object
    resources : all subject resources
    is_ratted: tells whether user has already rated target Subject
    comments: Target Subject comments
    comments_form: form for a new comment
    rate_form: form for a new rate
    page_title:
    """ 
    subject = get_object_or_404(Subject,slug=subject_slug)
    resources = subject.resource_set.all()
    page_title = subject.name
    is_ratted = False
    #dont't allow people to rate a subject more than once
    if request.user.subjectrate_set.filter(subject=subject):
        is_ratted=True
    rate_form = get_rate_form(Subject)()
    #save comment
    if request.method=="POST":
        if request.POST.get('action')=='comment':
            comments_form = CommentsForm(request.POST)
            if comments_form.is_valid():
                comments_form.save(user=request.user,subject=subject)
    comments= Comments.objects.filter(subject=subject).order_by('-date_comment')
    comments_form = CommentsForm()
    return render_to_response(template_name,locals(),context_instance=RequestContext(request))

@login_required
def show_professor(request,professor_slug,template_name="resources/professor.html"):
    """Show the target Professor
    @in: 
    template_name: the template (if not the default)
    professor_slug: identifies the professor
    request: current request object
    
    Context Variables{}:
    professor: Target Professor object
    subjects : all professor subjects
    is_ratted: tells whether user has already rated target Professor
    comments: Target Subject comments
    comments_form: form for a new comment
    rate_form: form for a new rate
    page_title:
    """ 
    professor = get_object_or_404(Professor,slug=professor_slug)
    subjects = professor.professor_subjects.all()
    page_title = professor.name
    
    is_ratted = False
    if request.user.professorrate_set.filter(professor=professor):
        is_ratted=True
        
    rate_form = get_rate_form(Professor)()
    if request.method=="POST":
        if request.POST.get('action')=='comment':
            comments_form = CommentsForm(request.POST)
            if comments_form.is_valid():
                comments_form.save(user=request.user,professor=professor)
    comments= Comments.objects.filter(professor=professor).order_by('-date_comment')
    comments_form = CommentsForm()
    return render_to_response(template_name,locals(),context_instance=RequestContext(request))

@login_required
def show_resource(request,resource_slug,template_name="resources/resource.html"):
    """Show the target Resource
    @in: 
    template_name: the template (if not the default)
    resource_slug: identifies the resource
    request: current request object
    
    Context Variables{}:
    resource: Target Resource object
    is_ratted: tells whether user has already rated target Resource
    comments: Target Subject comments
    comments_form: form for a new comment
    rate_form: form for a new rate
    page_title:
    """ 
    resource = get_object_or_404(Resource,slug=resource_slug)
    #avoid URL attempt to view deleted resource
    if resource.deleted:
        raise Http404
    is_ratted = False
    if request.user.resourcerate_set.filter(resource=resource):
        is_ratted=True
    #rate_form = ResourceRateForm()
    rate_form = get_rate_form(Resource)()
    #if request.method == 'POST':
    #    if request.POST.get('action')=='download':
    #        slug = request.POST.get('resource_slug','0')
    #        resource = get_object_or_404(Resource,slug=slug)
    #        if not Hit.objects.filter(resource=resource,user=request.user):
    #            resource.resource_hit.create(user=request.user)
    #        return HttpResponseRedirect('/media/uploads/'+resource.file.name)
    if request.method=="POST":
        if request.POST.get('action')=='comment':
            comments_form = CommentsForm(request.POST)
            if comments_form.is_valid():
                comments_form.save(user=request.user,resource = resource)
    comments= Comments.objects.filter(resource=resource).order_by('-date_comment')
    comments_form = CommentsForm()
    
    page_title = resource.title
    
    return render_to_response(template_name,locals(),context_instance=RequestContext(request))

@login_required
def show_subjects(request,template_name="resources/subjects.html"):
    subjects = Subject.objects.filter(deleted=False).order_by('period')
    page_title = "Materias"
    return render_to_response(template_name,locals(),context_instance=RequestContext(request))

@login_required
def show_professors(request,template_name="resources/professors.html"):
    professors = Professor.objects.filter(deleted=False).order_by('name')
    page_title = "Professores"
    try:
        page = int(request.GET.get('page',1))
    except ValueError:
        page = 1;
        
    paginator = Paginator(professors,settings.PRODUCTS_PER_PAGE)
    try:
        professors = paginator.page(page).object_list
    except (InvalidPage,EmptyPage):
        professors = paginator.page(1).object_list
        
    return render_to_response(template_name,locals(),context_instance=RequestContext(request))

@login_required
def results(request,template_name="resources.html"):
    q = request.GET.get('q','')
    try:
        page = int(request.GET.get('page',1))
    except ValueError:
        page = 1;
    words = utils._prepare_words(q)
    resources = Resource.objects.filter(deleted=False)
    for word in words:
        resources = resources.filter(Q(title__icontains=word)|
                                     Q(l_period__title__icontains=word)|
                                     Q(subject__name__icontains=word)|
                                     Q(subject__professor__name__icontains=word))
    
    
    paginator = Paginator(resources,settings.PRODUCTS_PER_PAGE)
    
    try:
        results = paginator.page(page).object_list
    except (InvalidPage,EmptyPage):
        results = paginator.page(1).object_list
    page_title = 'Resultados da Busca para:'+q
    return render_to_response(template_name,locals(),context_instance=RequestContext(request))

@login_required
def add_resource(request,template_name="resource_form.html"):
    form = ResourceForm()
    if request.method=='POST':
        value = unicode(request.FILES['file']._name)
        request.FILES['file']._name = utils.remover_acentos(value)
        form = ResourceForm(request.POST,request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.collaborator = request.user
            try:
                period = Period.objects.get(title='Não Informado')
                
            except:
                period = Period.objects.create()
            new.l_period = period
            if request.POST.get('professor'):
                new.professor = Professor.objects.get(id = request.POST.get('professor'))
            new.save()
            url = urlresolvers.reverse('resources_resource', args=[new.slug])
            return HttpResponseRedirect(url)
    return render_to_response(template_name,locals(),context_instance=RequestContext(request))



@login_required
def add_rating(request,object):
    form = get_rate_form(object)(request.POST)
    if form.is_valid():
        new_object = form.save(request.user,request.POST.get('slug'))
        
        new_rate = new_object.nota()
        response = simplejson.dumps({'succes':'True','new_rate':new_rate})
    else:
        response = simplejson.dumps({'succes':'False'})
    return HttpResponse(response, content_type = 'aplication/javascript; charset=utf8')

def add_resource_professor(request):
    if request.POST.get('subject'):
        subject = Subject.objects.get(id=request.POST.get('subject'))
        form = ResourceProfessorForm(subject)
        template = "resources/resource_professor.html"
        html = render_to_string(template,{'form':form})
        response = simplejson.dumps({'succes':'True','html':html})
    else:
        response = simplejson.dumps({'succes':'False'})
    return HttpResponse(response, content_type = 'aplication/javascript; charset=utf8')

@login_required
def download(request, resource_slug):
    r = Resource.objects.get(slug = resource_slug)
    #avoid URL attempt to view deleted resource
    if r.deleted:
        raise Http404
    ext = r.file.name.split('.')[-1]
    file = open(r.file.path,'r+')
    #file = open(r.file.file)
    #content = file.read()
    length = os.path.getsize(r.file.path)
    
    if not Hit.objects.filter(resource=r,user=request.user):
        r.resource_hit.create(user=request.user)
    
    wrapper = FileWrapper(file)
    filename = r.file.name.split('/')[-1]
    import mimetypes
    mime = mimetypes.guess_type(filename)
    response = HttpResponse(r.file.file, mimetype=mime[0])
    
    response['Content-Disposition'] = 'attachment; filename=' + filename
    response['Content-Length'] = length 
    return response