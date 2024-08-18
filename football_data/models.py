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
    year = models.IntegerField(editable=False, unique=True, null=True, blank=True)
    
    def __str__(self):
        return str(self.year)

    class Meta:
        ordering = ['year']


    


