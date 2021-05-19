from django.contrib import admin

from .models import MgmtUser

class MgmtUser_view(admin.ModelAdmin):
    list_display = ('name' , 'email' , 'auth', 'action', 'created')
admin.site.register(MgmtUser, MgmtUser_view)
