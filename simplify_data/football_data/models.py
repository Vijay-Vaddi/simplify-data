from django.db import models
import uuid

class Country(models.Model):
    code = models.CharField(max_length=10, null=True, blank=True)
    flag = models.URLField(null=True, blank=True)
    name = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Countries"
    
    def __str__(self) -> str:
        return self.name

