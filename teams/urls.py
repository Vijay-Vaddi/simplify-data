from django.urls import path
from . import views

urlpatterns = [
    path('teams/countries', views.teams_countries, name='teams_countries'),
    path('teams/information', views.team_info, name='team_info'),
    path('teams/seasons', views.team_seasons, name='teams_seasons'),   
]