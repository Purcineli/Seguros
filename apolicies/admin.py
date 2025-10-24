from django.contrib import admin
from apolicies.models import Apolice, TiposSeguros

class ApoliceAdmin(admin.ModelAdmin):
    list_display = ('numero', 'seguradora', 'tipo_seguro', 'status', 'data_inicio', 'data_fim', 'valor_seguro', 'segurado')
    search_fields = ('numero', 'seguradora', 'tipo_seguro', 'segurado__nome')
    list_filter = ('status', 'data_inicio', 'data_fim')
    ordering = ('-data_inicio',)

class TiposSegurosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'ativo', 'criado_em', 'atualizado_em')
    search_fields = ('nome', 'descricao')
    list_filter = ('ativo',)

    

admin.site.register(Apolice, ApoliceAdmin)
admin.site.register(TiposSeguros, TiposSegurosAdmin)
