from django.contrib import admin
from .models import Fixture, Periods, Score, Goal, League, Status
# Register your models here.

admin.site.register(Fixture)
admin.site.register(League)
admin.site.register(Status)
admin.site.register(Score)
admin.site.register(Goal)
admin.site.register(Periods)
