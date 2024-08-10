from django.db import models


class Country(models.Model):
    code = models.CharField(max_length=10)
    flag = models.URLField()
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "Countries"
    
    def __str__(self) -> str:
        return self.name

