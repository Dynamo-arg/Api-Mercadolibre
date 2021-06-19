from django.urls import path

from .views import views_home
from .views import views2
from .views import views_competencia
from .views import views_tendencias



urlpatterns = [
    path('', views_home.homepage, name='home'),
    path('login/', views2.loginPage, name='login'),
    path('register/', views2.registerPage, name='register'),
    path('logout/', views2.logoutUser, name='logout'),
    path('layout/', views2.homepage, name='layout'),
    path('competencia/', views_competencia.competencia, name='competencia'),
    path('tendencias/', views_tendencias.tendencias, name='tendencias'),
]

