from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
            #check whether query is a date and search corresponding match
            try:
                isdate = bool(datetime.strptime(query, "%Y-%m-%d"))
            except ValueError:
                isdate = False
            if isdate:
                date=datetime.strptime(query, "%Y-%m-%d").date()
                matchs = Match.objects.filter(Date__date=date)
            #if not a date search for team names or scores
            else :
                matchs = Match.objects.filter(Team1__Name__icontains=query).union(
                    Match.objects.filter(Team2__Name__icontains=query))
                #cherche les match selon un score
                scores = query.split("-")
                if len(scores)==2:
                    matchs = matchs.union(
                        Match.objects.filter(Score1__contains=scores[0], Score2__contains=scores[1])).union(
                            Match.objects.filter(Score2__contains=scores[0], Score1__contains=scores[1]))
                #cherche les matchs selon une opposition
                queries = query.split(" vs ")
                if len(queries)==2:
                    matchs = matchs.union(
                        Match.objects.filter(Team1__Name__icontains=queries[0],Team2__Name__icontains=queries[1])).union(
                            Match.objects.filter(Team2__Name__icontains=queries[0],Team1__Name__icontains=queries[1]))
            teams = Team.objects.filter(Name__icontains=query)
            newform = SearchForm()
            context = {"matchs" : matchs, "teams":teams, "form":newform}
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

@login_required
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

@login_required
def removeComment(request, pk):
    comment = Comment.objects.get(id=pk)
    matchId = comment.Match.id
    if request.user == comment.User:
        comment.delete()
    return HttpResponseRedirect(reverse('tournament:matchDetail',  args=[matchId]))

@login_required
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