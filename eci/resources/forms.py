# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import inlineformset_factory, ModelForm, BaseInlineFormSet
from eci.resources.models import *
from django.contrib.auth.models import User

class CommentsForm(forms.Form):
    comment = forms.CharField(widget = forms.Textarea)   
    def save(self,user,*args,**kwargs):
        if self.cleaned_data:
            try:
                if kwargs['resource']:
                    Comments.objects.create(author = user,resource=kwargs['resource'],comment=self.cleaned_data['comment'])
            except:
                pass
            
            try:
                if kwargs['professor']:
                    Comments.objects.create(author = user,professor=kwargs['professor'],comment=self.cleaned_data['comment'])
            except:
                pass
            
            try:
                if kwargs['subject']:
                    Comments.objects.create(author = user,subject=kwargs['subject'],comment=self.cleaned_data['comment'])
            except:
                pass

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        exclude =  ['slug','professor','collaborator','created','deleted','user_rate','hit']
    
    def __init__(self,*args,**kwargs):
        super(ResourceForm,self).__init__(*args,**kwargs)
        self.fields['title'].widget.attrs['class'] = 'text'
        self.fields['info'].widget.attrs['rows'] = '10'
    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1]
        if ext =='exe':
            raise forms.ValidationError('A extensão .exe não está sendo aceita no momento.')
        return file
        
#class ResourceRateForm(forms.ModelForm):
#    class Meta:
#        model = ResourceRate
#        exclude = ['user','resource']
#    
#    def save(self,user,slug,*args,**kwargs):
#        if self.cleaned_data:
#            resource = Resource.objects.get(slug=slug)
#            ResourceRate.objects.create(user = user,resource=resource,rate=self.cleaned_data['rate'])
#            return resource

def get_rate_form(object):
    if object == Resource:
        rate_model = ResourceRate
        type = 'resource'
    elif object == Subject:
        rate_model = SubjectRate
        type='subject'
    elif object == Professor:
        rate_model = ProfessorRate
        type = 'professor'
    
    class RateForm(forms.ModelForm):
        class Meta:
            model = rate_model
            exclude = ['user',type]
        
        def save(self,user,slug,*args,**kwargs):
            if self.cleaned_data:
                saved = object.objects.get(slug=slug)
                if object == Resource:
                    ResourceRate.objects.create(user = user,resource=saved,rate=self.cleaned_data['rate'])
                elif object == Subject:
                    SubjectRate.objects.create(user = user,subject=saved,rate=self.cleaned_data['rate'])
                elif object == Professor:
                    ProfessorRate.objects.create(user = user,professor=saved,rate=self.cleaned_data['rate'])
                return saved
    return RateForm

    
class ResourceProfessorForm(forms.Form):
    professor = forms.ModelChoiceField(queryset=Professor.objects.all())
    
    def __init__(self,subject, *args, **kwargs):
        super(ResourceProfessorForm, self).__init__(*args, **kwargs)
        self.fields['professor'].queryset = Professor.objects.filter(professor_subjects = subject)

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        exclude =  ['slug','collaborator','created','deleted','user_rate','professor_subjects']

class CheckProfessorForm(forms.Form):
    professor = forms.ModelChoiceField(queryset=Professor.objects.all())
    
    def __init__(self,ids, *args, **kwargs):
        super(CheckProfessorForm, self).__init__(*args, **kwargs)
        self.fields['professor'].queryset = Professor.objects.filter(id__in=ids)