from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='pass_index'),
    path('etudiant', views.get_etudiant, name='get_etudiant'),
    path('ue/<int:id>', views.get_ue, name='get_ue'),
    path('competence/<int:id>', views.get_competence, name='get_competence'),
    path('periode/<int:id>', views.get_periode, name='get_periode'),
    path('taf/<int:id>', views.get_taf, name='get_taf'),
    path('ue_suivi/<int:id>', views.get_ue_suivi, name='get_ue_suivi'),
    path('eval_competence/<int:id>', views.get_eval_competence, name='get_eval_competence'),
    path('formation/<int:id>', views.get_formation, name='get_formation'),
    path('obligation/<int:id>', views.get_obligation, name='get_obligation'),
]
