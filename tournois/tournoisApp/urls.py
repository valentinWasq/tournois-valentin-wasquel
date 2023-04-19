from django.urls import path
from . import views

app_name = 'tournament'
urlpatterns = [
    path('', views.home, name='home'),
    path('tournament/', views.tournamentList, name='tournamentList')
]