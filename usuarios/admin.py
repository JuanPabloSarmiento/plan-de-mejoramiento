from django.contrib import admin
from .models import Usuarios

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'edad', 'fecha_creacion')
    search_fields = ('nombre', 'correo')
    list_filter = ('edad',)

admin.site.register(Usuarios, UsuarioAdmin)
