from django.urls import path
from . import views

urlpatterns = [
    path('by-team', views.get_players_of_a_team, name='player_by_team'),
]