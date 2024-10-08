
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include("football_data.urls")),
    path('players/', include("players.urls")),
    path('fixtures/', include("fixtures.urls")),
    path('teams/', include("teams.urls")),
    path('admin/', admin.site.urls),
    
]
