from django.shortcuts import render
from django.http import HttpResponse
from .get_response import get_response
from .models import Country, EndpointTracker
from datetime import datetime, timedelta
from django.utils import timezone

def index(request):
    return HttpResponse("Hello, the app is working")

def countries(request):
     
    category = 'Countries and Seasons'
    enpoint_name = 'Countries'
    endpoint = "/v3/countries"

    endpoint, created = EndpointTracker.objects.get_or_create(
        name=enpoint_name, category=category, endpoint=endpoint
    ) 

    # if endpoint request exists
    if not created:
        # and if last request time > 1 day, clear all countries data
        if timezone.now() - endpoint.last_requested > timedelta(days=1):
            Country.objects.all().delete()
            print('deleting old data')
        else:
            # if last requested time <1 day no need to fetch data
            return HttpResponse('Data upto date')
    
    # make new request to endpoint and fetch data
    # if its first request from endpoint or time since last_request > 1
    countries = get_response(endpoint)
    print('Getting reponse and adding to table')
    
    for country_item in countries:
        country = Country(
            name = country_item['name'],
            code = country_item['code'],
            flag = country_item['flag'],
        )
        country.save()
    
    return HttpResponse("Countries saved")

def seasons(request):
    seasons = get_response()