from django.shortcuts import render
from django.http import HttpResponse
from .get_response import get_response, load_api_response
from .models import Country, EndpointTracker, Season, Team, Venue
from datetime import timedelta
from django.utils import timezone

def index(request):
    return HttpResponse("Hello, the app is working")

def countries(request):
     
    category = 'Countries and Seasons'
    enpoint_name = 'Countries'
    endpoint = "/v3/countries"

    endpoint_tracker, created = EndpointTracker.objects.get_or_create(
        name=enpoint_name, category=category, endpoint=endpoint
    ) 

    # if endpoint request exists
    if not created:
        # and if last request time > 1 day, clear all countries data
        if timezone.now() - endpoint_tracker.last_requested > timedelta(days=1):
            Country.objects.all().delete()
            print('deleting old data')
        else:
            # if last requested time <1 day no need to fetch data
            return HttpResponse('Data upto date')
    
    # make new request to endpoint and fetch data
    # if its first request from endpoint or time since last_request > 1
    countries = get_response(endpoint)
    
    for country_item in countries:
        name = country_item['name'].replace('-', ' ').title()
        country, created = Country.objects.get_or_create(
            name = name
        )

        # to ensure data stays with most info
        if country_item['code']:
            country.code = country_item['code'] 
        if country_item['flag']:
            country.flag = country_item['flag']
        country.save()
        

    return HttpResponse("Countries saved")

def seasons(request):

    category = 'Countries and Seasons'
    enpoint_name = 'Seasons'
    endpoint = "/v3/leagues/seasons"

    # endpoint_tracker, created = EndpointTracker.objects.get_or_create(
    #     name=enpoint_name, category=category, endpoint=endpoint
    # ) 

    # # if endpoint request exists
    # if not created:
    #     # and if last request time > 1 day, clear all countries data
    #     if timezone.now() - endpoint_tracker.last_requested > timedelta(days=1):
    #         Season.objects.all().delete()
    #         print('deleting old data')
    #     else:
    #         # if last requested time <1 day no need to fetch data
    #         return HttpResponse('Data upto date')
    
    seasons = get_response(endpoint)
    
    for season in seasons:  
        season = Season(
            year = season,
        )
        season.save()

    return HttpResponse('Seasons endpoint')


def team_info(request):
    category = 'Teams'
    enpoint_name = 'Teams Information'
    endpoint = "/v3/teams?country=England"

    # endpoint_tracker, created = EndpointTracker.objects.get_or_create(
    #     name=enpoint_name, category=category, endpoint=endpoint
    # ) 

    # # if endpoint request exists
    # if not created:
    #     # and if last request time > 1 day, clear all countries data
    #     if timezone.now() - endpoint_tracker.last_requested > timedelta(days=1):
    #         Season.objects.all().delete()
    #         print('deleting old data')
    #     else:
    #         # if last requested time <1 day no need to fetch data
    #         return HttpResponse('Data upto date')
    
    # team_response = get_response(endpoint)
    team_response= load_api_response()
    for team_item in team_response:
        # # get venue and team data from team info
        venue = team_item['venue']
        team = team_item['team']

        if venue['id'] is not None and type(venue['id']) is int:
            # create venue obj
            venue_obj, created = Venue.objects.get_or_create(id=venue['id'])    
            #  update values to team
            try:
                venue_obj.address=venue['address']
                venue_obj.name = venue['name']
                venue_obj.city = venue['city']
                venue_obj.capacity = venue['capacity']
                venue_obj.surface = venue['surface']
                venue_obj.image = venue['image']
                venue_obj.save()
                team_obj, created = Team.objects.get_or_create(id=team['id'])    
                team_obj.venue = venue_obj        
            except:
                    print('Something went wrong---',  venue_obj)
                
    
        team_obj, created = Team.objects.get_or_create(id=team['id'])    
        # team_obj.venue = venue_obj

        # # # create team and link to country if existed   
        country, created = Country.objects.get_or_create(name=team['country'])
        team_obj.country = country
        
        #  link team to venue link to team 
        team_obj.venue = venue_obj
        # # # update values to team
        team_obj.code=team['code']
        team_obj.founded = team['founded']
        team_obj.national = team['national']
        team_obj.logo = team['logo']
        team_obj.name = team['name']
        team_obj.save()
    
    return HttpResponse('Team and venue info retrieved')

def team_seasons(request):
    category = 'Teams'
    enpoint_name = 'Teams Seasons'
    endpoint = "/v3/teams/seasons?team=33"

    endpoint_tracker, created = EndpointTracker.objects.get_or_create(
        name=enpoint_name, category=category, endpoint=endpoint
    ) 

    # if endpoint request exists
    if not created:
        # and if last request time > 1 day, clear all countries data
        if timezone.now() - endpoint_tracker.last_requested > timedelta(days=1):
            Season.objects.all().delete()
            print('deleting old data')
        else:
            # if last requested time <1 day no need to fetch data
            return HttpResponse('Data upto date')
    
    team_id = 33
    team_seasons = get_response(endpoint)
    team = Team.objects.get(id=team_id)
    for season in team_seasons:
        season, created = Season.objects.get_or_create(year=season)
        season.save()
        team.seasons.add(season)
    
    team.save()

    return HttpResponse('Teams seasons saved')

def teams_countries(request):
    category = 'Teams'
    enpoint_name = 'Teams countries'
    endpoint = "/v3/teams/countries"
    # endpoint = "/v3/teams?league=39&season=2019"


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
    #         return HttpResponse('Teams countries Data upto date')
    
    # make new request to endpoint and fetch data
    # if its first request from endpoint or time since last_request > 1
    countries = get_response(endpoint)
    print(countries)
    
    for country_item in countries:
        name = country_item['name'].replace('-', ' ').title()
        country, created = Country.objects.get_or_create(
            name = name
        )

        # to ensure current data not replaced by Null or ''
        if country_item['code']:
            country.code = country_item['code'] 
        if country_item['flag']:
            country.flag = country_item['flag']
        country.save()
    
    return HttpResponse("Teams countries saved")

