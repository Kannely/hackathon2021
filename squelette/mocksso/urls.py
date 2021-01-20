from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='sso_index'),
    path('login', views.do_login, name='sso_login'),
    path('user', views.get_user, name='sso_get_user'),
    path('logout', views.do_logout, name='sso_logout'),
]
