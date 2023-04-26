from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime

from .models import Tournament, Pool, Match, Team, Comment
from .forms import CommentForm, SearchForm

# Create your views here.
def home(request):
    if request.method == "POST":
        searchForm = SearchForm(request.POST)
        if searchForm.is_valid():
            query = searchForm.cleaned_data['query']
            #check whether query is a date
            try:
                isdate = bool(datetime.strptime(query, "%Y/%m/%d"))
            except ValueError:
                isdate = False
            if isdate:
                matchs = Match.objects.filter(Date__date=datetime.strptime(query, "%Y/%m/%d").date())
            #if not a date search for team names or scores
            else :
                matchs = Match.objects.filter(Team1__Name__icontains=query).union(
                    Match.objects.filter(Team2__Name__contains=query)).union(
                        Match.objects.filter(Score1__contains=query)).union(
                            Match.objects.filter(Score2__contains=query))
            teams = Team.objects.filter(Name__icontains=query)
            context = {"matchs" : matchs, "teams":teams}
            template_name = "tournois/SearchResults.html"
            return render(request, template_name, context)
    else :
        searchForm = SearchForm()
        template_name = 'tournois/Home.html'
    return render(request, template_name,{"form":searchForm})

def tournamentList(request):
    template_name = 'tournois/TournamentList.html'
    allTournament = Tournament.objects.all()
    context = {'allTournament' : allTournament}
    return render(request, template_name, context)

def tournamentDetail(request, pk):
    template_name = 'tournois/TournamentDetail.html'
    tournament = Tournament.objects.get(id=pk)
    context = {'tournament': tournament}
    return render(request, template_name, context)

def poolDetail(request, pk):
    template_name = 'tournois/PoolDetail.html'
    pool = Pool.objects.get(id=pk)
    canGenerate = (len(pool.Teams.all()) == pool.Tournois.NBTeamPerPool)
    context = {'pool': pool, 'canGenerate':canGenerate}
    return render(request, template_name, context)

def generateMatchs(request, pk):
    pool = Pool.objects.get(id=pk)
    if (len(pool.match_set.all()) == 0) and (len(pool.Teams.all()) == pool.Tournois.NBTeamPerPool) and (request.user.is_superuser):
        pool.createAllMatch()
        pool.save()
    return HttpResponseRedirect(reverse('tournament:poolDetail',  args=[pool.id]))

def matchDetail(request, pk):
    template_name = 'tournois/MatchDetail.html'
    match = Match.objects.get(id=pk)
    commentForm = CommentForm()
    context = {'match': match, 'commentForm' : commentForm}
    return render(request, template_name, context)

def teamDetail(request, pk):
    template_name = 'tournois/TeamDetail.html'
    team = Team.objects.get(id=pk)
    context = {'team': team}
    return render(request, template_name, context)

def addComment(request):
    if (request.method == 'GET') or (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('tournament:home'))
    form = CommentForm(request.POST)
    if (form.is_valid()):
        user = request.user
        date = timezone.now()
        content = form.cleaned_data["Content"]
        matchId = request.POST["MatchId"]  
        match = Match.objects.get(id=matchId)
        comment = Comment(User=user, Date=date, Content=content, Match=match)
        comment.save()
        return HttpResponseRedirect(reverse('tournament:matchDetail',  args=[matchId]))
    else :
        return HttpResponseRedirect(reverse('tournament:home'))

def removeComment(request, pk):
    comment = Comment.objects.get(id=pk)
    matchId = comment.Match.id
    if request.user == comment.User:
        comment.delete()
    return HttpResponseRedirect(reverse('tournament:matchDetail',  args=[matchId]))

def editComment(request, pk):
    comment = Comment.objects.get(id=pk)
    if comment.User != request.user:
        return HttpResponseRedirect(reverse('tournament:matchDetail',  args=[comment.Match.id]))
    if request.method == 'GET':
        template_name = 'tournois/EditComment.html'
        commentForm = CommentForm()
        context = {"Comment" : comment, "commentForm": commentForm}
        return render(request, template_name, context)
    else:
        form = CommentForm(request.POST)
        if (form.is_valid()):
            comment.Content = form.cleaned_data["Content"]
            comment.save()
        return HttpResponseRedirect(reverse('tournament:matchDetail',  args=[comment.Match.id]))
    
def testMap(request):
    template = "tournois/TestMap.html"
    context = {"longitude" : 1.433333, "lattitude" : 43.6}
    return render(request, template, context)