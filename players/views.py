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

    # add date checking logic to truncate the data. 

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


def get_player_stats(request):
     
    category = 'Players'
    enpoint_name = 'Player statistics by league'
    endpoint = "/v3/players?league=39&season=2020"
    # endpoint =  "/v3/players?team=33&season=2020"
    # add date checking logic to truncate the data. 

    # player_league_stats = get_response(endpoint, 'player_league_stats.json')
    player_league_stats = load_api_response('player_league_stats.json')
    
    for player_item in player_league_stats:
        player = player_item['player']
        player_stats = player_item['statistics']

        nationality = player.pop('nationality')
        birth = player.pop('birth')

        if player['id'] is not None:
            player_obj, created = Player.objects.update_or_create(id=player['id'], 
                                                                  defaults=player)
            player_obj.save()

            if nationality is not None:
                country, created = Country.objects.get_or_create(name=nationality)
                country.save()
                player_obj.nationality = country
                player_obj.save()

            try:
                if birth is not None:
                    country = birth.pop('country')
                    country, created = Country.objects.get_or_create(name=country)
                    birth_obj, created = Birth.objects.update_or_create(date=birth['date'],
                                                place=birth['place'],country=country, player=player_obj)
                    birth_obj.save()
                else:
                    print('here', birth)
            except:
                print('Something went wrong')
    
    return HttpResponse("Players saved")
