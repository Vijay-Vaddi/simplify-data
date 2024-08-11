from django.contrib import admin
from .models import Country, EndpointTracker

admin.site.register(Country)
admin.site.register(EndpointTracker)