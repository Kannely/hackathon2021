from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='pass_index'),
    path('etudiant', views.get_etudiant, name='pass_get_etudiant'),
    path('ue/<int:id>', views.get_ue, name='pass_get_ue'),
    path('all_ue', views.get_all_ue, name='pass_all_ue'),
    path('competence/<int:id>', views.get_competence, name='pass_get_competence'),
    path('all_competence', views.get_all_competence, name='pass_all_competence'),
    path('periode/<int:id>', views.get_periode, name='pass_get_periode'),
    path('taf/<int:id>', views.get_taf, name='pass_get_taf'),
    path('ue_suivi/<int:id>', views.get_ue_suivi, name='pass_get_ue_suivi'),
    path('eval_competence/<int:id>', views.get_eval_competence, name='pass_get_eval_competence'),
    path('formation/<int:id>', views.get_formation, name='pass_get_formation'),
    path('obligation/<int:id>', views.get_obligation, name='pass_get_obligation'),
]
