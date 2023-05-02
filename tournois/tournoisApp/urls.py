from django.urls import path
from . import views

app_name = 'tournament'
urlpatterns = [
    path('',                        views.home,             name='home'),               # home page, simple view
    path('tournament/',             views.tournamentList,   name='tournamentList'),     # list of tournaments, simple view
    path('tournament/<int:pk>',     views.tournamentDetail, name='tournamentDetail'),   # detail of a tournament, simple view
    path('pool/<int:pk>',           views.poolDetail,       name='poolDetail'),         # detail of a pool, simple view
    path('match/<int:pk>',          views.matchDetail,      name='matchDetail'),        # detail of a match, simple view
    path('team/<int:pk>',           views.teamDetail,       name='teamDetail'),         # detail of a team, simple view
    path('addComment/',             views.addComment,       name='addComment'),         # add a comment, only post (redirect to matchDetail if successful, or home otherwise)
    path('removeComment/<int:pk>',  views.removeComment,    name='removeComment'),      # remove a comment, only post (redirect to matchDetail)
    path('editComment/<int:pk>',    views.editComment,      name='editComment'),        # edit a comment, get => view, post redirect to matchDetail
    path('generateMatchs/<int:pk>', views.generateMatchs,   name='generateMatchs'),     # call pool.createAllMatch if condition met, redirect to poolDetail

    path('testMap/',                views.testMap,          name='testMap'),
    path('editMatch/<int:pk>',      views.editMatch,        name='editMatch') # pk == -1 => create new match
]