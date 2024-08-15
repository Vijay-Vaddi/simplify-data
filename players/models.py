from django.db import models
from football_data.models import Country, Season, Team

class Player(models.Model):
    id = models.IntegerField(editable=False, unique=True, 
                             primary_key=True, blank=False, null=False)
    name = models.CharField(max_length=64, null=True, blank=True)
    firstname = models.CharField(max_length=64, null=True, blank=True)
    lastname = models.CharField(max_length=64, null=True, blank=True)
    age = models.IntegerField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, 
                                null=True, blank=True)
    height = models.CharField(max_length=64, blank=True, null=True)
    weight = models.CharField(max_length=64, blank=True, null=True)
    photo = models.URLField(null=True, blank=True)
    seasons = models.ManyToManyField(Season, related_name='players')
    team = models.ForeignKey(Team, null=True, blank=True, 
                                on_delete=models.SET_NULL)
    number = models.IntegerField(null=True, blank=True)
    position = models.CharField(max_length=64, null=True, blank=True)
    nationality = models.ForeignKey(Country, on_delete=models.SET_NULL, 
                                null=True, blank=True, related_name="players")
    injured = models.BooleanField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return str(self.name)

class Birth(models.Model):
    date = models.DateField(null=True, blank=True)
    place = models.CharField(max_length=64, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, 
                                null=True, blank=True, related_name="birth")
    # not considering that a same birthday/time can belong to many players even though 
    # its possible. So setting one-to-one for simplicity for now. 
    player = models.OneToOneField(Player, null=True, blank=True, 
                                  on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']

    def __str__(self) -> str:
        return  str(self.date)
