from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='front_index'),
    path('about', views.about, name='front_about'),
]
