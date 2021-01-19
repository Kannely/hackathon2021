from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='front_index'),
    path('bus', views.bus, name='front_bus'),
    path('movies', views.movies, name='front_movies'),
    path('animals', views.animals, name='front_animals'),
    path('vue', views.vue, name='front_vue'),
    path('chart', views.chart, name='front_chart'),

    path('login', auth_views.LoginView.as_view(
        template_name='login.html'
    ), name="front_login"),
    path('logout', auth_views.LogoutView.as_view(
        template_name='logout.html'
    ), name="front_logout"),
    path('synthesis', views.synthesis, name='front_synthesis'),
    path('obligations', views.obligations, name='front_obligations'),
    path('skills', views.skills, name='front_skills'),
    path('courses', views.courses, name='front_courses'),
]
