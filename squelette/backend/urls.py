from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='back_index'),
    path('synthese', views.get_synthese, name='synthese'),
]
