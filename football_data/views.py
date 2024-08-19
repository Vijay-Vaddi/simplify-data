from django.shortcuts import render
from django.http import HttpResponse
from .utils import get_response, load_api_response, time_to_fetch
from .models import Country, Season 

def index(request):
    # send an async requet here for once a day or once an hour. 

    # call views from here to check if its to fetch new data and update
    # pass request object. 
    # return update status. 
    

    return HttpResponse("Hello, the app is working")

def countries(request):
    category = 'Countries and Seasons'
    enpoint_name = 'Countries'
    endpoint = "/v3/countries"

    if time_to_fetch(category, enpoint_name, endpoint):
        Country.objects.all().delete()
    else:
        return HttpResponse('Items up to date')
    
    # if its first request from endpoint or time since last_request > 1
    # countries = get_response(endpoint, 'countries.json')
    countries = load_api_response('countries.json')

    if save_countries(countries):
        return HttpResponse("Countries saved")
    else:
        return HttpResponse('Something went wrong')
    
def seasons(request):
    category = 'Countries and Seasons'
    enpoint_name = 'Seasons'
    endpoint = "/v3/leagues/seasons"
    
    if time_to_fetch(category, enpoint_name, endpoint):
        Season.objects.all().delete()
    else:
        return HttpResponse('Items up to date')
    seasons = get_response(endpoint)
    
    for season in seasons:  
        season = Season.objects.get_or_create(year=season)

    return HttpResponse('Seasons endpoint')

def save_countries(countries):
    try:
        for country_item in countries:
            name = country_item['name'].replace('-', ' ').title()
            country, created = Country.objects.get_or_create(name=name)
            
            # to ensure current data not replaced by Null or ''
            if country_item['code']:
                country.code = country_item['code'] 
            if country_item['flag']:
                country.flag = country_item['flag']
            country.save()
    except:
        return False
    return True    

