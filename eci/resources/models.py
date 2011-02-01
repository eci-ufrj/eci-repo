# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.files.storage import FileSystemStorage
import os
from eci import settings
from django.contrib import admin
from django.db.models.signals import post_save
from django.db.models import Count
from django.template.loader import render_to_string



class Period(models.Model):
    title = models.CharField('Período',max_length='20',default='Não informado')
    
    def __unicode__(self):
        return self.title
    class Meta:
        verbose_name = "Período"
        
class Subject(models.Model):
    PERIOD_CHOICES = ((1,'1o'),
                      (2,'2o'),
                      (3,'3o'),
                      (4,'4o'),
                      (5,'5o'),
                      (6,'6o'),
                      (7,'7o'),
                      (8,'8o'),
                      (9,'9o'),
                      (10,'10o'),
                      )
    
    TYPE_CHOICES = (('o','Obrigatória'),
                    ('e','Eletiva'),
                    )
    name = models.CharField('Nome',max_length='60')
    slug = models.SlugField(max_length=60, unique=True,blank=True)
    collaborator = models.ForeignKey(User,verbose_name='Colaborador',related_name='subject_collaborator',blank=True,null=True)
    created= models.DateTimeField('Data de criação',auto_now_add=True)
    info = models.TextField('Informações',blank=True)
    deleted = models.BooleanField(verbose_name="Indicador de exclusão", default=False)
    user_rate = models.ManyToManyField(User,through="SubjectRate")
    period = models.IntegerField('Período',choices=PERIOD_CHOICES,default=1)
    type = models.CharField(choices = TYPE_CHOICES,default='o',max_length=2)
    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table='subject'
        verbose_name= 'Matéria'
        ordering = ('name',)
    
    def save(self,*args,**kwargs):
        if not self.id:
            unique = False
            self.slug = slugify(self.name)
            while not unique:
                try:
                    Subject.objects.get(slug=self.slug)
                    self.slug+='_'
                except:
                    unique=True
        super(Subject, self).save(*args, **kwargs)
        
    @models.permalink
    def get_absolute_url(self):
        return ('resources_subject', (), {'subject_slug': self.slug})
    
    def nota(self):
        sr = self.subjectrate_set.all()
        sr_length = len(sr)
        if sr:
            rate = 0.0
            for r in sr:
                rate += r.rate
            rate = rate/(sr_length*1.0) 
            return str(rate)+'( '+str(sr_length)+' voto(s) )'
        else:
            return 'Sem Nota'
        
        
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name','nota','period','info','created','collaborator',)
        
class Professor(models.Model):
    name = models.CharField('Nome',max_length='60')
    slug = models.SlugField(max_length=60, unique=True,blank=True)
    collaborator = models.ForeignKey(User,verbose_name='Colaborador',related_name='professor_collaborator',blank=True,null=True)
    created = models.DateTimeField('Data de criação',auto_now_add=True)
    info = models.TextField('Informações',blank=True)
    deleted = models.BooleanField(verbose_name="Indicador de exclusão", default=False)
    user_rate = models.ManyToManyField(User,through="ProfessorRate")
    professor_subjects = models.ManyToManyField(Subject)
    
    class Meta:
        db_table='professor'
        verbose_name = 'Professores'
    
    def __unicode__(self):
        return self.name
        
    def save(self,*args,**kwargs):
        if not self.id:
            unique = False
            self.slug = slugify(self.name)
            while not unique:
                try:
                    Professor.objects.get(slug=self.slug)
                    self.slug+='_'
                except:
                    unique=True
        super(Professor, self).save(*args, **kwargs)
        
    @models.permalink
    def get_absolute_url(self):
        return ('resources_professor', (), {'professor_slug': self.slug})
    
    def nota(self):
        pr = self.professorrate_set.all()
        pr_length = len(pr)
        if pr:
            rate = 0.0
            for r in pr:
                rate += r.rate
            rate = rate/(pr_length*1.0) 
            return str(rate)+'( '+str(pr_length)+' voto(s) )'
        else:
            return 'Sem Nota'
        
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('name','nota','info','created','collaborator','deleted')
    fields = ('name','info','professor_subjects',)
    
file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))

class ActiveResourceManager(models.Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(ActiveResourceManager,self).get_query_set().filter(deleted=False)
    
class Resource(models.Model):
    title = models.CharField('Título',max_length='60')
    subject = models.ForeignKey(Subject,verbose_name="Matéria")
    professor = models.ForeignKey(Professor,blank=True,null=True)
    l_period = models.ForeignKey(Period,verbose_name='Período lecionado',blank=True,null=True)
    info = models.TextField('Informações',blank=True)
    slug = models.SlugField(max_length=60, unique=True,blank=True)
    file = models.FileField(upload_to="%Y-%m", storage=file_storage, verbose_name="Arquivo")
    created = models.DateTimeField('Data de criação',auto_now_add=True)
    deleted = models.BooleanField(verbose_name="Indicador de exclusão", default=False)
    user_rate = models.ManyToManyField(User,through="ResourceRate")
    collaborator = models.ForeignKey(User,verbose_name='Colaborador',related_name='resource_collaborator',blank=True,null=True)
    hit = models.ManyToManyField(User,through="Hit",related_name='hit')
    
    
    active = ActiveResourceManager()
    objects = models.Manager()


    
    def get_file_display(self):
        return self.file.name.split('/')[-1]
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = "Recurso"
        ordering = ('created',)
    def month_hits(self):
        hits = self.resource_hit.all()
        hits = hits.filter(date__year=datetime.date.today().year).filter(date__month=datetime.date.today().month)
        total = len(hits)
        return total
    def nota(self):
        rr = self.resourcerate_set.all()
        rr_length = len(rr)
        if rr:
            rate = 0.0
            for r in rr:
                rate += r.rate
            rate = round(rate/(rr_length*1.0),1) 
            return str(rate)+'( '+str(rr_length)+' voto(s) )'
        else:
            return 'Sem Nota'
        
    def save(self,*args,**kwargs):
        if not self.id:
            unique = False
            self.slug = slugify(self.title)
            while not unique:
                try:
                    Resource.objects.get(slug=self.slug)
                    self.slug+='_'
                except:
                    unique=True
        super(Resource, self).save(*args, **kwargs)    
        
    @models.permalink
    def get_absolute_url(self):
        return ('resources_resource', (), {'resource_slug': self.slug})    

    
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title','file','nota','subject','month_hits','l_period','info','created','collaborator','deleted')
    fields = ('title','file','subject','professor','l_period','info',)
    
class Hit(models.Model):
    resource = models.ForeignKey(Resource,related_name='resource_hit')
    user = models.ForeignKey(User,related_name='user_hit')
    date = models.DateTimeField('Data de download',auto_now_add=True)
    
    
    
class ResourceRate(models.Model):
    RATE_CHOICES = ((5,'Excelente'),
                    (4,'Bom'),
                    (3,'Razoável'),
                    (2,'Ruim'),
                    (1,'Péssimo'),
                    )
    rate = models.IntegerField('Nota',choices=RATE_CHOICES,default=5)
    resource = models.ForeignKey(Resource,blank=True,null=True)
    user = models.ForeignKey(User,blank=True,null=True)
    
    def __unicode__(self):
        return self.user.username+' deu nota '+str(self.rate)+' para '+self.resource.title
    
    class Meta:
        verbose_name = "Nota de Recurso"
        verbose_name_plural = "Notas de Recursos"   
        ordering = ('rate',)
        
class ProfessorRate(models.Model):
    RATE_CHOICES = ((5,'Excelente'),
                    (4,'Bom'),
                    (3,'Razoável'),
                    (2,'Ruim'),
                    (1,'Péssimo'),
                    )
    rate = models.IntegerField('Nota',choices=RATE_CHOICES,default=5)
    professor = models.ForeignKey(Professor)
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.user.username+' deu nota '+str(self.rate)+' para '+self.professor.name
    
    class Meta:
        verbose_name = "Nota de Professor"
        verbose_name_plural = "Notas de Professores"
        ordering = ('rate',)      

class SubjectRate(models.Model):
    RATE_CHOICES = ((5,'Excelente'),
                    (4,'Bom'),
                    (3,'Razoável'),
                    (2,'Ruim'),
                    (1,'Péssimo'),
                    )
    rate = models.IntegerField('Nota',choices=RATE_CHOICES,default=5)
    subject = models.ForeignKey(Subject)
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.user.username+' deu nota '+str(self.rate)+' para '+self.subject.name
    
    class Meta:
        verbose_name = "Nota de Matéria"
        verbose_name_plural = "Notas de Matérias"
        ordering = ('rate',) 

class Profile(models.Model):
    YEAR_CHOICES = ((0,'2004'),
                    (1,'2005'),
                    (2,'2006'),
                    (3,'2007'),
                    (4,'2008'),
                    (5,'2009'),
                    (6,'2010'),
                    (7,'2011'),
                    )
    
    user = models.ForeignKey(User, unique=True)
    nome = models.CharField('Nome',max_length='40',blank=True)
    url = models.URLField('Website',blank=True)
    year = models.IntegerField(choices = YEAR_CHOICES,default = 7,verbose_name="Ano de ingresso")
    avatar = models.ImageField(upload_to='images/avatars/',blank=True)
    
    def top(self):
        users = User.objects.filter(is_active=True)
        top = users.annotate(count=Count('resource_collaborator')).order_by('-count')[:5]
        if self.user in top:
            return True
        else:
            return False
    def __unicode__(self):
        return self.user.username + ' ' + self.user.email
    
    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"
        
    @models.permalink    
    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })

class Comments(models.Model):
    resource = models.ForeignKey(Resource,verbose_name="Arquivo",blank=True,null=True)
    subject = models.ForeignKey(Subject,verbose_name="Matéria",blank=True,null=True)
    professor = models.ForeignKey(Professor,verbose_name="Professor",blank=True,null=True)
    
    author = models.ForeignKey(User,verbose_name="Autor")
    comment = models.TextField(max_length=300,verbose_name="Comentário")
    date_comment = models.DateTimeField('Dia e hora',auto_now_add=True)

    def __unicode__(self):
        return 'Comentário de '+self.author.username+' as '+unicode(self.date_comment)
    
def on_user_register(sender, **kwargs):
    '''Create a profile for new users.'''
    
    if kwargs['created']:
        
        user = kwargs['instance']
        profile = Profile()
        try:
            user.get_profile()
        except:
            profile.user = user
            profile.save()
            ctx_dict = {}
            subject = render_to_string('registration/activation_email_subject.txt',
                                       ctx_dict)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            
            message = render_to_string('registration/activation_email.txt',
                                       ctx_dict)
            user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
        
        

        
post_save.connect(on_user_register, User)