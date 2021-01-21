from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='back_index'),
    path('synthesis', views.get_synthesis, name='back_synthesis'),
    path('comp_gen', views.get_comp_gen, name='back_comp_gen'),
    path('ue_per_year', views.get_ue_per_year, name='back_ue_per_year'),
    path('jetons', views.get_jetons, name='back_jetons'),
    path('ects', views.get_ects, name='back_ects'),
    path('obligations', views.get_obligations, name='back_obligations'),
    path('ue_list', views.all_ue, name='back_all_ue'),
    path('ue/<int:pk>', views.get_ue_details, name='back_ue_details'),
    path('comp_list', views.all_competence, name='back_all_competence'),
    path('comp/<int:pk>', views.get_comp_details, name='back_comp_details'),
]
