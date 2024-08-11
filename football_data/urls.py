from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('countries', views.countries, name='countries'),
    path('seasons', views.seasons, name='seasons'),
    

]