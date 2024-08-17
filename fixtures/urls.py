from django.urls import path
from . import views

urlpatterns = [
    path('by-date', views.get_fixture_by_date, name='fixture_by_date'),
]