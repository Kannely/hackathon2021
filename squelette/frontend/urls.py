from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='front_index'),
    path('about', views.about, name='front_about'),
    path('base', views.base, name='front_base'),
    path('animals', views.animals, name='front_animals'),
    path('vue', views.vue, name='front_vue'),
]
