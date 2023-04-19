from django.urls import path
from . import views

app_name = 'tournament'
urlpatterns = [
    path('', views.home, name='home'),
    path('tournament/', views.tournamentList, name='tournamentList'),
    path('tournament/<int:pk>', views.tournamentDetail, name='tournamentDetail'),
    path('pool/<int:pk>', views.poolDetail, name='poolDetail')
]