from django.contrib import admin
from .models import *

class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('user', 'nom', 'prenom')

class PeriodeAdmin(admin.ModelAdmin):
    list_display = ('code',)
    
class FormationAdmin(admin.ModelAdmin):
    list_display = ('code',)
    
class ObligationsAdmin(admin.ModelAdmin):
    list_display = ('stage', 'etranger', 'ielts', 'lv1', 'lv2')

class TAFAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom')

class CompetenceAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom')
    
class UEAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'responsable', 'creneau')

# Register your models here.
admin.site.register(Etudiant, EtudiantAdmin)
admin.site.register(TAF, TAFAdmin)
admin.site.register(Periode, PeriodeAdmin)
admin.site.register(Formation, FormationAdmin)
admin.site.register(Obligations, ObligationsAdmin)
admin.site.register(SuivreUE)
admin.site.register(EvalCompetence)
admin.site.register(Competence, CompetenceAdmin)
admin.site.register(UE, UEAdmin)
