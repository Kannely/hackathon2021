from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='front_index'),
    path('bus', views.bus, name='front_bus'),
    path('movies', views.movies, name='front_movies'),
    path('animals', views.animals, name='front_animals'),
    path('vue', views.vue, name='front_vue'),
    path('chart', views.chart, name='front_chart'),

    path('synthesis', views.synthesis, name='front_synthesis'),
    path('obligations', views.obligations, name='front_obligations'),
    path('skills', views.skills, name='front_skills'),
    path('courses', views.courses, name='front_courses'),
]
