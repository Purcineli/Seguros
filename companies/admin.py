from django.contrib import admin
from companies.models import Companies  

class CompaniesAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome')
    search_fields = ('codigo', 'nome')
    ordering = ('codigo',)

admin.site.register(Companies, CompaniesAdmin)
