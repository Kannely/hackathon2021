from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='back_index'),
    path('synthesis', views.get_synthesis, name='back_synthesis'),
]
