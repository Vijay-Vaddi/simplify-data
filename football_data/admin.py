from django.contrib import admin
from .models import Country, EndpointTracker, Season

admin.site.register(Country)
admin.site.register(EndpointTracker)
admin.site.register(Season)