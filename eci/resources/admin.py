# -*- coding: utf-8 -*-
from django.contrib import admin
from eci.resources.models import *
class UserAdmin(admin.ModelAdmin):
    list_display =('email','is_active','last_login','date_joined','is_staff',)
    actions = ['ativar_usuarios']
    
    def ativar_usuarios(self, request, queryset):
        rows_updated = queryset.update(is_active=True)
        if rows_updated == 1:
            message_bit = "1 usuário foi"
        else:
            message_bit = "%s usuários foram " % rows_updated
        self.message_user(request, "%s marcados como ativos com sucesso." % message_bit)

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Professor,ProfessorAdmin)
admin.site.register(Resource,ResourceAdmin)
admin.site.register(SubjectRate)
admin.site.register(ProfessorRate)
admin.site.register(ResourceRate)
admin.site.register(Period)
admin.site.register(Hit)
admin.site.unregister(User)
admin.site.register(User,UserAdmin)