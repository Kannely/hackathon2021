from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='pass_index'),
]
