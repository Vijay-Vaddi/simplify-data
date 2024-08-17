from django.shortcuts import render
from django.http import HttpResponse
from football_data.get_response import get_response, load_api_response
from .models import Fixture, League, Score, Goal, Periods, Status
from football_data.models import Venue

# Create your views here.

def get_fixture_by_date(request):
    
    endpoint = "/v3/fixtures?date=2024-08-15"

    # response = get_response(endpoint, "fixtures_by_date.json")
    fixtures = load_api_response("fixtures_by_date.json")

    for fixture_item in fixtures:
        fixture = fixture_item['fixture']

        # pop and save periods
        periods = fixture.pop('periods')
        period_obj, created = Periods.objects.update_or_create(first=periods['first'],
                                                           second=periods['second'])
        period_obj.save()

        # pop and save venue
        venue = fixture.pop('venue')
        if venue['id'] is not None:
            print(venue)
            venue_obj, created = Venue.objects.update_or_create(venue_id=venue['id'], defaults=venue)
            venue_obj.save()
        else:
            venue_obj, created = Venue.objects.update_or_create(name=venue['name'], 
                                                             city=venue['city'])
            venue_obj.save()
        
        status = fixture.pop('status')
        status_obj, created = Status.objects.update_or_create(long=status['long'],
                                                          short=status['short'],
                                                          elapsed=status['elapsed'])
        status_obj.save()

        fixture_obj, created = Fixture.objects.update_or_create(id=fixture['id'], 
                                                defaults={**fixture, 'periods':period_obj, 
                                                'status':status_obj, 'venue':venue_obj})

    
        fixture_obj.save()

    return HttpResponse('Fixtures saved')