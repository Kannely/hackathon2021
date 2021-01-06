from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='back_index'),
    path('/actor/<str:name>/<str:surname>/', views.actor, name='back_actor'),
]
