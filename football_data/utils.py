from .models import EndpointTracker
from datetime import timedelta
from django.utils import timezone
from .models import Country

import http.client
import api_key
import json
import os 
from pathlib import Path

connection = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")

headers = {
    'x-rapidapi-key': api_key.api_key,
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
}

def get_response(endpoint, file_name):
       
    connection.request("GET", endpoint, headers=headers)
    result = connection.getresponse()
    response_body = result.read()
    # # print('response_body',response_body) 
    decoded_data = response_body.decode(encoding="utf-8")
  
    # # deserialize the json data to a python dictionary 
    reponse_dict = json.loads(decoded_data)

    # # extract reponse part of the data
    response = reponse_dict['response']
    file_path = os.path.join(os.curdir, file_name)

    with open(file_path, 'w') as file:
        json.dump(response, file, indent=4)

    return response

def load_api_response(file_name='teams_info.json'):
    file_path = Path('.') / file_name
    null = None
    if file_path.exists():
        with open(file_path, 'r') as file:
            return json.load(file)
        
def time_to_fetch(category, endpoint_name, endpoint): 
    
    endpoint_tracker, created = EndpointTracker.objects.get_or_create(
            name=endpoint_name, category=category, endpoint=endpoint) 
    
    # new request
    if created:
        return True
    # if endpoint request exists
    # and if last request time > 1 day, clear all countries data
    if timezone.now() - endpoint_tracker.last_requested > timedelta(days=1):  
            return True

    return False

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