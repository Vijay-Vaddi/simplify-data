from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True, unique=True)
    code = models.CharField(max_length=10, null=True, blank=True)
    flag = models.URLField(null=True, blank=True)
    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']
    
    def __str__(self) -> str:
        return str(self.name)

class EndpointTracker(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    endpoint = models.CharField(max_length=256, unique=True)
    last_requested = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Endpoints"

    def __str__(self) -> str:
        return str(self.name)
    
class Season(models.Model):
    year = models.IntegerField(editable=False, unique=True)
    
    def __str__(self):
        return str(self.year)


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

        # constrints = [
        #         models.UniqueConstraint(fields=['name', 'city'],
        #                                 name='unique_venue')
        # ]

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
    


