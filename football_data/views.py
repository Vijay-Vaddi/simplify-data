from django.shortcuts import render
from django.http import HttpResponse
from .get_response import get_response
from .models import Country, EndpointTracker, Season
from datetime import datetime, timedelta
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
        name = country_item['name'].replace('-', ' ')
        country, created = Country.objects.get_or_create(
            name = name
        )
        country.code = country_item['code'] 
        country.flag = country_item['flag']
        country.save()

    return HttpResponse("Countries saved")

def seasons(request):

    category = 'Countries and Seasons'
    enpoint_name = 'Seasons'
    endpoint = "/v3/leagues/seasons"

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
    
    seasons = get_response(endpoint)
    
    for season in seasons:  
        season = Season(
            year = season,
        )
        season.save()

    return HttpResponse('Seasons endpoint')





# def teams_countries(request):
#     print('inside teams countries')
#     category = 'Teams'
#     enpoint_name = 'Teams countries'
#     endpoint = "/v3/teams/countries"

#     endpoint_tracker, created = EndpointTracker.objects.get_or_create(
#         name=enpoint_name, category=category, endpoint=endpoint
#     ) 

#     # if endpoint request exists
#     if not created:
#         # and if last request time > 1 day, clear all countries data
#         if timezone.now() - endpoint_tracker.last_requested > timedelta(days=1):
#             Country.objects.all().delete()
#             print('deleting old data')
#         else:
#             # if last requested time <1 day no need to fetch data
#             return HttpResponse('Teams countries Data upto date')
    
#     # make new request to endpoint and fetch data
#     # if its first request from endpoint or time since last_request > 1
#     countries = get_response(endpoint)
#     print(countries)
#     for country_item in countries:
#         name = country_item['name'].replace('-', ' ')
#         country, created = Country.objects.get_or_create(
#             name = name
#         )
#         country.code = country_item['code'] 
#         country.flag = country_item['flag']
#         country.save()
    
#     return HttpResponse("Teams countries saved")
