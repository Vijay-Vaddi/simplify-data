from django.contrib import admin
from .models import Country, EndpointTracker, Season, Venue, Team

admin.site.register(Country)
admin.site.register(EndpointTracker)
admin.site.register(Season)
admin.site.register(Team)
admin.site.register(Venue)