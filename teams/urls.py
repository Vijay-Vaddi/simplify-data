from django.urls import path
from . import views

urlpatterns = [
    path('countries', views.teams_countries, name='teams_countries'),
    path('information', views.team_info, name='team_info'),
    path('seasons', views.team_seasons, name='teams_seasons'),   
]