
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include("football_data.urls")),
    path('players/', include("players.urls")),
    
    path('admin/', admin.site.urls),
    
]
