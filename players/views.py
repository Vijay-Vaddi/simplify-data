from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from football_data.utils import get_response, load_api_response, time_to_fetch
from football_data.models import Country
from teams.models import Team
from .models import Player, Birth

def get_players_of_a_team(request):
    # check if team item is passed in url
    if 'team' in request.GET:
        team_id=str(request.GET['team'])
    else:
        # default team MANU
        team_id = str(33)  
    
    category = 'Players'
    endpoint_name = 'Player'
    endpoint = "/v3/players/squads?team="+team_id

    if time_to_fetch(category, endpoint_name, endpoint):
        Player.objects.all().delete()
    else:
        return JsonResponse({'message':'Items up to date'})

    # add date checking logic to truncate the data. 
    squad = load_api_response('players_by_squad.json')[0]

    team = squad['team']
    players = squad['players']    

    team_obj, created = Team.objects.update_or_create(id=team['id'],
                                                defaults=team)

    for player in players:
        if player['id'] is not None:
            player_obj, created = Player.objects.update_or_create(id=player['id'],
                                defaults=player) 
            player_obj.team = team_obj
            player_obj.save()

    return JsonResponse({'message':"Players saved"})


def get_player_stats(request):
    #ignore stats from both endpoints but only player info is saved
    category = 'Players'
    enpoint_name = 'Player statistics by league'
    # endpoint = "/v3/players?league=39&season=2020"
    endpoint =  "/v3/players?team=33&season=2020"
    
    # add date checking logic to truncate the data. 
    if time_to_fetch(category, enpoint_name, endpoint):
        Player.objects.all().delete()
    else:
        return JsonResponse({'message':'Items up to date'})

    # player_league_stats = get_response(endpoint, 'player_team_stats.json')
    player_league_stats = load_api_response('player_team_stats.json')
    
    for player_item in player_league_stats:
        player = player_item['player']
        player_stats = player_item['statistics']

        nationality = player.pop('nationality')
        birth = player.pop('birth')

        if player['id'] is not None:
            player_obj, created = Player.objects.update_or_create(id=player['id'], 
                                                                  defaults=player)
            
            if nationality is not None:
                country, created = Country.objects.get_or_create(name=nationality)
                player_obj.nationality = country
                player_obj.save()

            try:
                if birth is not None:
                    country = birth.pop('country')
                    country, _ = Country.objects.get_or_create(name=country)
                    birth_obj, _ = Birth.objects.update_or_create(date=birth['date'],
                                                place=birth['place'], country=country, player=player_obj)
                    birth_obj.save()
                else:
                    print('Issue with item--', birth)
            except Exception as e:
                print('Something went wrong', e)
    
    return JsonResponse({'message':"Players saved"})
