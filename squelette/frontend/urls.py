from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='front_index'),
    path('bus', views.bus, name='front_bus'),
    path('movies', views.movies, name='front_movies'),
    path('vue', views.vue, name='front_vue'),
    path('chart', views.chart, name='front_chart'),

    path('login', views.login, name="front_login"),
    path('logout', views.logout, name="front_logout"),
    path('synthesis', views.synthesis, name='front_synthesis'),
    path('obligations', views.obligations, name='front_obligations'),
    path('skills', views.skills, name='front_skills'),
    path('courses', views.courses, name='front_courses'),
]
