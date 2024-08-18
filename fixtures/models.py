from django.db import models
from football_data.models import Country
from teams.models import Venue, Team


class Fixture(models.Model):
    id = models.IntegerField(primary_key=True, null=False, blank=False,
                             editable=False)
    referee = models.CharField(max_length=64, null=True, blank=True)

    timezone = models.CharField(max_length=16, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)

    # relationships with other tables 
    status = models.ForeignKey('Status', on_delete=models.SET_NULL, 
                               null=True, blank=True)
    league = models.ForeignKey('League', on_delete=models.SET_NULL, 
                               null=True, blank=True, related_name='fixtures')
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, 
                               null=True, blank=True, related_name='fixtures')
    periods = models.ForeignKey('Periods', on_delete=models.SET_NULL, 
                               null=True, blank=True, related_name='fixtures')
    home_team = models.ForeignKey(Team, on_delete=models.SET_NULL, 
                               null=True, blank=True, related_name='fixtures_home')
    away_team = models.ForeignKey(Team, on_delete=models.SET_NULL, 
                               null=True, blank=True, related_name='fixtures_away')
    
    score = models.ForeignKey('Score', on_delete=models.SET_NULL, 
                               null=True, blank=True, related_name='fixtures_score')

    class Meta:
        ordering = ['date']

    def __str__(self) -> str:
        return f"{self.home_team.name} - vs - {self.away_team.name}"
    
class Status(models.Model):
    long = models.CharField(max_length=16, null=True, blank=True)
    short = models.CharField(max_length=16, null=True, blank=True)
    elapsed = models.CharField(max_length=16, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Status"    
        ordering = ['long']
    
    def __str__(self) -> str:
        return str(self.long)


class Periods(models.Model): 
    first  = models.IntegerField(null=True, blank=True)
    second = models.IntegerField(null=True, blank=True)    

    class Meta:
        verbose_name_plural = "Periods"
    
    def __str__(self) -> str:
        return str(self.first)


class League(models.Model):
    id = models.IntegerField(primary_key=True, null=False, blank=False,
                            editable=False)
    name = models.CharField(max_length=64, null=True, blank=True)           
    country = models.ForeignKey(Country, null=True, blank=True,
                                related_name='leagues', on_delete=models.SET_NULL)
    logo = models.URLField(null=True, blank=True, max_length=128) 
    flag = models.URLField(null=True, blank=True, max_length=128)
    season = models.IntegerField(null=True, blank=True)          
    round = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        ordering = ['name']


class Score(models.Model):
    half_time = models.ForeignKey('Goal', null=True, blank=True,
                                related_name='half_time', on_delete=models.SET_NULL)
    full_time = models.ForeignKey('Goal', null=True, blank=True,
                                related_name='full_time', on_delete=models.SET_NULL)
    penalty =  models.ForeignKey('Goal', null=True, blank=True,
                                related_name='penalty_time', on_delete=models.SET_NULL)
    extratime = models.ForeignKey('Goal', null=True, blank=True,
                                related_name='extra_time', on_delete=models.SET_NULL)
    
    
    def __str__(self) -> str:
        return f"HT: {self.half_time}, FT: {self.full_time}, Pen: {self.penalty}, Extra: {self.extratime}" 


class Goal(models.Model):
    home = models.IntegerField(null=True, blank=True)
    away = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return str((self.home, self.away))