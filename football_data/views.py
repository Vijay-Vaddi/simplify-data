from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .utils import get_response, load_api_response, time_to_fetch, save_countries
from .models import Country, Season 
from teams.views import team_info, team_seasons, teams_countries
from players.views import get_players_of_a_team, get_player_stats
from fixtures.views import get_fixture_by_date
import json

def index(request):
    # call views from here to check if its to fetch new data and update
    # pass request object. 
    # return update status.
    # access the 'message' field and use the message within the index view

    countries_response = countries(request)
    response_data = json.loads(countries_response.content)
    message = response_data.get('message')
    messages.success(request, message)

    # regular checking for fixture update 
    fixture_message = get_fixture_by_date(request)
    response_data=json.loads(fixture_message.content)
    message = response_data.get('message')
    messages.success(request, message)

    # regular checking for players of a single team
    players_of_team = get_players_of_a_team(request)
    response_data = json.loads(players_of_team.content)
    message = response_data.get('message')
    messages.success(request, message)
    
    # regular checking for teams in a country
    team_venue = team_info(request)
    response_data = json.loads(team_venue.content)
    message = response_data.get('message')
    messages.success(request, message)

    # can call other endpoints from here to check for updates 
    # or let the endpoints be called manually 

    return render(request, 'index.html') 
    
def countries(request):
    category = 'Countries and Seasons'
    endpoint_name = 'Countries'
    endpoint = "/v3/countries"

    if time_to_fetch(category=category, endpoint=endpoint, endpoint_name=endpoint_name):
        # if one day passed, delete items in table and fetch anew
        Country.objects.all().delete()
    else:
        return JsonResponse({'message':'Countries up to date'})
    
    # if its first request from endpoint or time since last_request > 1
    # countries = get_response(endpoint, 'countries.json')
    countries = load_api_response('countries.json')

    if save_countries(countries):
        return JsonResponse({"message":"Countries saved"})
    else:
        return JsonResponse({"message":'Something went wrong'})
    
def seasons(request):
    category = 'Countries and Seasons'
    enpoint_name = 'Seasons'
    endpoint = "/v3/leagues/seasons"
    
    if time_to_fetch(category, enpoint_name, endpoint):
        Season.objects.all().delete()
    else:
        return JsonResponse({'message':'Items up to date'})
    seasons = get_response(endpoint, 'countries_seasons.json')
    
    for season in seasons:  
        season = Season.objects.get_or_create(year=season)

    return JsonResponse({"message":"Seasons saved"})



