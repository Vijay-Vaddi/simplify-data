from django.http import HttpResponse, JsonResponse
from football_data.utils import get_response, load_api_response, time_to_fetch
from .models import Fixture, League, Score, Goal, Periods, Status, Country
from teams.models import Team, Venue
from datetime import datetime, timedelta


def get_fixture_by_date(request):
    # check if particular date is passed
    if 'date' in request.GET:
        date_to_fetch=request.GET['date']
    else:
        # else fetch from prev day's date
        prev_day = datetime.today() - timedelta(days=1)
        date_to_fetch = prev_day.strftime("%Y-%m-%d") 
        
    endpoint_name = "Fixture by date"
    category = "Fixtures"    
    endpoint = "/v3/fixtures?date="+date_to_fetch
    
    # check if a new unique request is being made
    if time_to_fetch(category, endpoint_name, endpoint):
        # Since fixture items need to be appended, db tables can stay as is.
        pass
    else:
        return JsonResponse({'message':'Fixtures up to date'})
    
    fixtures = get_response(endpoint, "fixtures_by_date.json")
    fixtures = load_api_response("fixtures_by_date.json")

    for fixture_item in fixtures:
        fixture = fixture_item['fixture']

        # pop and save periods
        periods = fixture.pop('periods')
        period_obj, _ = Periods.objects.update_or_create(first=periods['first'],
                                                           second=periods['second'])

        # pop and save venue
        venue = fixture.pop('venue')
        if venue['id'] is not None:
            venue_obj, _ = Venue.objects.update_or_create(venue_id=venue['id'], defaults=venue)
        else:
            venue_obj, _ = Venue.objects.update_or_create(name=venue['name'], city=venue['city'])
        
        # pop and save status
        status = fixture.pop('status')
        status_obj, _ = Status.objects.update_or_create(long=status['long'], short=status['short'],
                                                          elapsed=status['elapsed'])

        # save league 
        league = fixture_item['league']
        country = league.pop('country')

        country_obj, _ = Country.objects.update_or_create(name=country)
        league_obj, _ = League.objects.update_or_create(id=league['id'], 
                                                        defaults=league)
        league_obj.country = country_obj
        #save teams
        teams = fixture_item['teams']
        home_team, away_team = teams['home'], teams['away'] 
        
        # ignoring winner item as its a calculated item
        home_team.pop('winner')
        away_team.pop('winner')

        # save home and away teams
        home_team_obj, _ = Team.objects.update_or_create(id=home_team['id'], defaults=home_team)
        away_team_obj, _ = Team.objects.update_or_create(id=away_team['id'], defaults=away_team)
        
        # save fixture goals
        scores = fixture_item['score']
        half_time, _ = Goal.objects.update_or_create(home=scores['halftime']['home'], 
                                                     away=scores['halftime']['away'])
        full_time, _ = Goal.objects.update_or_create(home=scores['fulltime']['home'], 
                                                     away=scores['fulltime']['away'])
        penalty, _ = Goal.objects.update_or_create(home=scores['penalty']['home'],
                                                      away=scores['penalty']['away'])
        extratime, _ = Goal.objects.update_or_create(home=scores['extratime']['home'], 
                                                     away=scores['extratime']['away'])
        
        scores_obj, _ = Score.objects.update_or_create(half_time=half_time, full_time=full_time,
                                                    penalty=penalty, extratime=extratime)

        fixture_obj, _ = Fixture.objects.update_or_create(id=fixture['id'], 
                                                defaults={**fixture, 'periods':period_obj, 
                                                'status':status_obj, 'venue':venue_obj, 
                                                'league':league_obj, 'home_team':home_team_obj,
                                                'away_team':away_team_obj, 'score':scores_obj})


    return JsonResponse({'message':'Fixtures saved'})