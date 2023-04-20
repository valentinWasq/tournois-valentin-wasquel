from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from .models import Tournament, Pool, Match, Team, Comment
from .forms import CommentForm

# Create your views here.
def home(request):
    template_name = 'tournois/Home.html'
    return render(request, template_name)

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
    if (request.method == 'GET'):
        print("c'est un get")
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