from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='back_index'),
    path('synthesis', views.get_synthesis, name='back_synthesis'),
    path('comp_gen', views.get_comp_gen, name='back_comp_gen'),
]
