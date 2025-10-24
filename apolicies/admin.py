from django.contrib import admin
from apolicies.models import Apolice

class ApoliceAdmin(admin.ModelAdmin):
    list_display = ('numero', 'seguradora', 'tipo', 'status', 'data_inicio', 'data_fim', 'valor_seguro', 'segurado')
    search_fields = ('numero', 'seguradora', 'tipo', 'segurado__nome')
    list_filter = ('status', 'data_inicio', 'data_fim')
    ordering = ('-data_inicio',)

admin.site.register(Apolice, ApoliceAdmin)
