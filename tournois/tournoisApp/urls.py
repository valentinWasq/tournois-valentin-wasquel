from django.urls import path
from . import views

app_name = 'tournament'
urlpatterns = [
    path('', views.home, name='home'),
    path('tournament/', views.tournamentList, name='tournamentList'),
    path('tournament/<int:pk>', views.tournamentDetail, name='tournamentDetail'),
    path('pool/<int:pk>', views.poolDetail, name='poolDetail'),
    path('match/<int:pk>', views.matchDetail, name='matchDetail'),
    path('team/<int:pk>', views.teamDetail, name='teamDetail'),
    path('addComment/', views.addComment, name='addComment'),
    path('removeComment/<int:pk>', views.removeComment, name='removeComment'),
    path('editComment/<int:pk>', views.editComment, name='editComment')
]