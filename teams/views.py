from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from football_data.utils import get_response, load_api_response, time_to_fetch, save_countries
from .models import Venue, Team
from football_data.models import Country, Season

# get all teams information from a country
# if ALL teams information to be fetched, first fetch all countries from teams_countries 
# and then pass to teams_info
# from ALL teams, ALL players can be fetched using get_players_of_team. 

def team_info(request):
    # check if country item is passed in url
    if 'country' in request.GET:
        country=request.GET['country']
    else:
        # default country
        country = 'England' 

    category = 'Teams'
    endpoint_name = 'Teams Information'
    endpoint = "/v3/teams?country="+country

    if time_to_fetch(category, endpoint_name, endpoint):
        Team.objects.all().delete()
    else:
        return JsonResponse({'message':'Items up to date'})

    # team_response = get_response(endpoint,'teams_info.json')
    team_response= load_api_response('teams_info.json')
    
    for team_item in team_response:
        # # get venue and team data from team info
        venue = team_item['venue']
        team = team_item['team']

        if venue['id'] is not None:
            try:
                defaults = { key:val for key, val in venue.items() }
                # create venue obj
                venue_obj, created = Venue.objects.update_or_create(venue_id=venue['id'], defaults=defaults)    
                # venue_obj.__dict__.update(defaults)
                team_obj, created = Team.objects.get_or_create(id=team['id'])    
                team_obj.venue = venue_obj            
            except Exception as e:
                print('At venue', venue, 'Error', e)
        team_obj, _ = Team.objects.get_or_create(id=team['id'])

        # create team and link to country if existed   
        country, _ = Country.objects.get_or_create(name=team.pop('country'))
        team_obj.country = country
        
        # link team to venue link to team 
        # update values to team
        team_defaults = {key:val for key, val in team.items()}
        team_obj.__dict__.update(team_defaults)
        team_obj.save()
    
    return JsonResponse({'message':'Team and venue info updated'})

def team_seasons(request):
    category = 'Teams'
    enpoint_name = 'Teams Seasons'
    endpoint = "/v3/teams/seasons?team=33"

    if time_to_fetch(category, enpoint_name, endpoint):
        Season.objects.all().delete()
    else:
        return JsonResponse({'message':'Items up to date'})
    
    team_id = 33
    team_seasons = get_response(endpoint)
    team = Team.objects.get(id=team_id)
    for season in team_seasons:
        season, created = Season.objects.get_or_create(year=season)
        team.seasons.add(season)
    
    team.save()

    return JsonResponse({'message':'Teams seasons saved'})

def teams_countries(request):
    category = 'Teams'
    enpoint_name = 'Teams countries'
    endpoint = "/v3/teams/countries"

    if time_to_fetch(category, enpoint_name, endpoint):
        Country.objects.all().delete()
    else:
        return JsonResponse({'message':'Items up to date'})
    # countries = get_response(endpoint, 'teams_countries.json')
    countries = load_api_response('teams_countries.json')

    if save_countries(countries):
        return JsonResponse({'message':"Teams countries saved"})
    else:
        return JsonResponse({'message':'Something went wrong'}) 
