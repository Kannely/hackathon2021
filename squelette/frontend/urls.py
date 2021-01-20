from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='front_index'),
    path('bus', views.bus, name='front_bus'),
    path('movies', views.movies, name='front_movies'),
    path('vue', views.vue, name='front_vue'),
]
