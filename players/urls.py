from django.urls import path
from . import views

urlpatterns = [
    path('by-team', views.get_players_of_a_team, name='team_players'),
    path('player-stats', views.get_player_stats, name='plays_from_stats'),
]