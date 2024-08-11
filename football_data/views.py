from django.shortcuts import render
from django.http import HttpResponse
from .get_response import get_response
from .models import Country

def index(request):
    return HttpResponse("Hello, the app is working")

def countries(request):
    items_to_fetch = "/v3/countries" 
    countries = get_response(items_to_fetch)
    
    # unique items filter


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