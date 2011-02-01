# -*- coding: utf-8 -*-
from django.contrib import admin
from eci.resources.models import *
from django.contrib.sites.models import Site
from django.contrib.auth.models import *
from django.core.mail import send_mail
from settings import DEFAULT_FROM_EMAIL
class UserAdmin(admin.ModelAdmin):
    list_display =('username','email','is_active','last_login','date_joined','is_staff',)
    actions = ['ativar_usuarios','desativar_usuarios']
    
    def ativar_usuarios(self, request, queryset):
        old_activation_status ={}
        for user in queryset:
            if user.is_active == False:
                old_activation_status[user.username] = True
        rows_updated = queryset.update(is_active=True)
        for user in queryset:
            if old_activation_status.__contains__(user.username):
                if old_activation_status[user.username] == user.is_active:
                    send_mail('Repositório ECI - Sua conta foi aceita!',
                              'Parabéns!\n\nSua conta foi aceita pela administração do site.\nAproveite para personalizar seu perfil agora em : eci.inoa.com.br/profiles/edit/\n\nAtt,\nEquipe Repositório ECI',
                               DEFAULT_FROM_EMAIL,
                               [user.email], fail_silently=True)

                     
        if rows_updated == 1:
            message_bit = "1 usuário foi marcado como ativo com sucesso."
        else:
            message_bit = "%s usuários foram marcados como ativos com sucesso." % rows_updated
        
            
        self.message_user(request, message_bit)
        
    def desativar_usuarios(self, request, queryset):
        rows_updated = queryset.update(is_active=False)
        if rows_updated == 1:
            message_bit = "1 usuário foi marcado como desativado com sucesso."
        else:
            message_bit = "%s usuários foram marcados como desativados com sucesso." % rows_updated
        
            
        self.message_user(request, message_bit)

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Professor,ProfessorAdmin)
admin.site.register(Resource,ResourceAdmin)
admin.site.register(SubjectRate)
admin.site.register(ProfessorRate)
admin.site.register(ResourceRate)
admin.site.register(Period)
admin.site.register(Hit)
admin.site.unregister(User)
admin.site.register(Profile)
admin.site.register(Comments)
admin.site.register(User,UserAdmin)
admin.site.unregister(Site)
admin.site.unregister(Group)
