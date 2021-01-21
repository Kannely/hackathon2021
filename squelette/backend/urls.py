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
]
