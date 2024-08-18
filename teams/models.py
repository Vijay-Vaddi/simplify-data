from django.db import models
from football_data.models import Country, Season

class Venue(models.Model):
    venue_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=64, null=True, blank=True)
    address = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    surface = models.CharField(max_length=32, null=True, blank=True )
    image = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        ordering = ['name']


class Team(models.Model):
    id = models.IntegerField(editable=False, unique=True, 
                             primary_key=True, blank=False, null=False)
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=32, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, 
                                null=True, blank=True)  
    founded = models.IntegerField(null=True, blank=True)
    national = models.BooleanField(null=True, blank=True)
    logo = models.URLField(null=True, blank=True)
    seasons = models.ManyToManyField(Season, related_name='teams')
    venue = models.ForeignKey(Venue, null=True, blank=True, on_delete=models.SET_NULL,
                              related_name='teams')

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return str(self.name)