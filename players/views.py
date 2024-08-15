from django.shortcuts import render
from django.http import HttpResponse
from football_data.get_response import get_response, load_api_response
from football_data.models import EndpointTracker, Country, Season, Team 
from datetime import timedelta
from django.utils import timezone
from .models import Player, Birth

def get_players_of_a_team(request):
     
    category = 'Players'
    enpoint_name = 'Player'
    endpoint = "/v3/players/squads?team=33"

    # endpoint_tracker, created = EndpointTracker.objects.get_or_create(
    #     name=enpoint_name, category=category, endpoint=endpoint
    # ) 

    # # if endpoint request exists
    # if not created:
    #     # and if last request time > 1 day, clear all countries data
    #     if timezone.now() - endpoint_tracker.last_requested > timedelta(days=1):
    #         Country.objects.all().delete()
    #         print('deleting old data')
    #     else:
    #         # if last requested time <1 day no need to fetch data
    #         return HttpResponse('Data upto date')
    
    # make new request to endpoint and fetch data
    # if its first request from endpoint or time since last_request > 1
    # players = get_response(endpoint,'players_by_squad.json')

    squad = load_api_response('players_by_squad.json')[0]
    print(type(squad))

    team = squad['team']
    players = squad['players']    

    team_obj, created = Team.objects.update_or_create(id=team['id'],
                                                name = team['name'],
                                                logo = team['logo'])
    team_obj.save()


    for player in players:
        if player['id'] is not None:
            player_obj, created = Player.objects.update_or_create(id=player['id'],
                                name = player['name'], 
                                age = player['age'], 
                                number = player['number'] ,
                                position = player['position'], 
                                photo = player['photo']) 
            player_obj.team = team_obj
            player_obj.save()

    return HttpResponse("Players saved")
