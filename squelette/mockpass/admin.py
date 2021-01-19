from django.contrib import admin
from .models import *

class CompetenceAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom')

# Register your models here.
admin.site.register(Etudiant)
admin.site.register(TAF)
admin.site.register(Periode)
admin.site.register(Formation)
admin.site.register(Obligations)
admin.site.register(SuivreUE)
admin.site.register(EvalCompetence)
admin.site.register(Competence, CompetenceAdmin)
admin.site.register(UE)
