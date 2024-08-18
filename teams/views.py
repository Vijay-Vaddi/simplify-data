from django.shortcuts import render
from django.http import HttpResponse
from football_data.utils import get_response, load_api_response
from .models import Venue, Team
from football_data.models import Country, Season
from football_data.views import save_coutries

def team_info(request):
    category = 'Teams'
    enpoint_name = 'Teams Information'
    endpoint = "/v3/teams?country=Germany"

    team_response = get_response(endpoint,'teams_info.json')
    team_response= load_api_response('teams_info.json')
    
    for team_item in team_response:
        # # get venue and team data from team info
        venue = team_item['venue']
        team = team_item['team']

        if venue['id'] is not None:
            defaults = { key:val for key, val in venue.items() }
            # create venue obj
            venue_obj, created = Venue.objects.update_or_create(id=venue['id'], defaults=defaults)    
            
            team_obj, created = Team.objects.get_or_create(id=team['id'])    
            team_obj.venue = venue_obj            
        
        team_obj, created = Team.objects.get_or_create(id=team['id'])    

        # create team and link to country if existed   
        country, created = Country.objects.get_or_create(name=team.pop('country'))
        team_obj.country = country
        
        # link team to venue link to team 
        team_obj.venue = venue_obj
        # update values to team
        team_defaults = {key:val for key, val in team.items()}
        team_obj.__dict__.update(team_defaults)
        team_obj.save()
    
    return HttpResponse('Team and venue info retrieved')

def team_seasons(request):
    category = 'Teams'
    enpoint_name = 'Teams Seasons'
    endpoint = "/v3/teams/seasons?team=33"

    team_id = 33
    team_seasons = get_response(endpoint)
    team = Team.objects.get(id=team_id)
    for season in team_seasons:
        season, created = Season.objects.get_or_create(year=season)
        team.seasons.add(season)
    
    team.save()

    return HttpResponse('Teams seasons saved')

def teams_countries(request):
    category = 'Teams'
    enpoint_name = 'Teams countries'
    endpoint = "/v3/teams/countries"

    countries = get_response(endpoint, 'teams_countries.json')

    if save_coutries(countries):
        return HttpResponse("Teams countries saved")
    else:
        return HttpResponse('Something went wrong') 
