from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import user_passes_test

from .models import Tournament, Pool, Match, Team, Comment, Point
from .forms import CommentForm, SearchForm, MatchForm

# Create your views here.
def chart(pk):
    label1=[]
    data1=[]
    data11=[]

    pool=Pool.objects.get(id=pk)
    allmatch=pool.match_set.all()
    allteam=Team.objects.all()
    for match in allmatch:
        date=str(match.Date)
        label1.append([match.Team1.Name, match.Team2.Name, date[0:10]])
        data1.append(match.Score1)
        data11.append(match.Score2)


    label2=[]
    data2=[]
    label4=[]
    data4=[]
    data3=[]

    for teams,score in pool.getTeamsAndScores().items():
        label4.append(teams.Name)
        data4.append(score)

    teamsAndScores= pool.getTeamsAndScores()
    allmatch=pool.match_set.all()
    for team in allteam:
        scoreTeam=0
        scoreEncaisse=0
        for match in allmatch:
            if match.Team1==team:
                scoreTeam=+match.Score1
                scoreEncaisse=+match.Score2
            if match.Team2==team:
                scoreTeam=+match.Score2
                scoreEncaisse=+match.Score1
        label2.append(team.Name)
        data2.append(scoreTeam)
        data3.append({"x":scoreEncaisse,"y":scoreTeam,"r":teamsAndScores[team]})
   
    


    context=[label1,data1,data11,label2,data2,data3,label4,data4]
    #context= {"label1":label1,"data1":data1,"data11":data11, "label2":label2,"data2":data2,"label4":label4,"data4":data4}
    return context


def home(request):
    menue = [['Accueil', 'tournament:home'], ['Liste des tournois', 'tournament:tournamentList']]
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
            matchs=matchs.order_by("Date")
            teams = Team.objects.filter(Name__icontains=query)
            newform = SearchForm()
            context = {"matchs" : matchs, "teams":teams, "form":newform, 'menue': menue}
            template_name = "tournois/SearchResults.html"
            return render(request, template_name, context)
    else :
        searchForm = SearchForm()
        template_name = 'tournois/Home.html'
    return render(request, template_name,{"form":searchForm, "menue": menue})

def tournamentList(request):
    menue = [['Accueil', 'tournament:home'], ['Liste des tournois', 'tournament:tournamentList']]
    template_name = 'tournois/TournamentList.html'
    allTournament = Tournament.objects.all()
    context = {'allTournament' : allTournament, "menue" : menue}
    return render(request, template_name, context)

def tournamentDetail(request, pk):
    menue = [['Accueil', 'tournament:home'], ['Liste des tournois', 'tournament:tournamentList']]
    template_name = 'tournois/TournamentDetail.html'
    tournament = get_object_or_404(Tournament,id=pk)
    context = {'tournament': tournament, "menue": menue}
    return render(request, template_name, context)

def poolDetail(request, pk):
    template_name = 'tournois/PoolDetail.html'
    pool = get_object_or_404(Pool,id=pk)
    canGenerate = (len(pool.Teams.all()) == pool.Tournois.NBTeamPerPool)
    contextchart=chart(pk)
    menue = [['Accueil', 'tournament:home'], ['Liste des tournois', 'tournament:tournamentList'], [pool.Tournois.Name, "tournament:tournamentDetail", pool.Tournois.id]]
    context = {'pool': pool, 'canGenerate':canGenerate, 'label1':contextchart[0], 'data1':contextchart[1], 'data11':contextchart[2], 'label2':contextchart[3], 'data2':contextchart[4],'data3':contextchart[5], 'label4':contextchart[6],'data4':contextchart[7], 'menue':menue}



    return render(request, template_name, context)

def generateMatchs(request, pk):
    pool = get_object_or_404(Pool,id=pk)
    if (len(pool.match_set.all()) == 0) and (len(pool.Teams.all()) == pool.Tournois.NBTeamPerPool) and (request.user.is_superuser):
        pool.createAllMatch()
        pool.save()
    return HttpResponseRedirect(reverse('tournament:poolDetail',  args=[pool.id]))

"""
    This view displays the tree of the knockout phase of the tournament
    The view is integrated to the TournamentDetail template
"""
def generateMatchTree(request, pk):
    tournament = get_object_or_404(Tournament,id=pk)
    tournament.generateNextRound(2) 
    tournament.save()
    return HttpResponseRedirect(reverse('tournament:tournamentDetail', args=[tournament.id]))


def matchDetail(request, pk):
    template_name = 'tournois/MatchDetail.html'
    match = get_object_or_404(Match,id=pk)
    commentForm = CommentForm()
    menue = [['Accueil', 'tournament:home'], ['Liste des tournois', 'tournament:tournamentList']]
    if (match.Tournament):
        menue += [[match.Tournament.Name, 'tournament:tournamentDetail', match.Tournament.id]]
    elif (match.Pool): # sometimes, match doesn't have a tournament but are in a pool belonging to a tournament
        if (match.Pool.Tournois):
            menue += [[match.Pool.Tournois.Name, 'tournament:tournamentDetail', match.Pool.Tournois.id]]
    if (match.Pool): # lors des eliminatoir, certain match n'ont pas de pool
        menue += [['Poule ' + str(match.Pool.index), 'tournament:poolDetail', match.Pool.id]]
    context = {'match': match, 'commentForm' : commentForm, "menue": menue}
    return render(request, template_name, context)

def teamDetail(request, pk):
    template_name = 'tournois/TeamDetail.html'
    team = get_object_or_404(Team,id=pk)
    matchs = Match.objects.filter(Team1__id__contains=pk).union(Match.objects.filter(Team2__id__contains=pk))
    matchs = matchs.order_by("Date")
    first_match = matchs[0] #pour le menu, poule et tournoi de son premier match (le dernier n'aura pas forcément de poules)
    menue = [['Accueil', 'tournament:home'], ['Liste des tournois', 'tournament:tournamentList']]
    if (first_match):#while creating a pool, a team can have no matchif (match.Tournament):
        if(first_match.Tournament):
            menue += [[first_match.Tournament.Name, 'tournament:tournamentDetail', first_match.Tournament.id]]
        elif (first_match.Pool): # sometimes, first_match doesn't have a tournament but are in a pool belonging to a tournament
            if (first_match.Pool.Tournois):
                menue += [[first_match.Pool.Tournois.Name, 'tournament:tournamentDetail', first_match.Pool.Tournois.id]]
        if (first_match.Pool): # lors des eliminatoir, certain first_match n'ont pas de pool
            menue += [['Poule ' + str(first_match.Pool.index), 'tournament:poolDetail', first_match.Pool.id]]
    context = {'team': team, "matchs":matchs, "first":first_match, "menue": menue}
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
        menue = [['Accueil', 'tournament:home'], ['Liste des tournois', 'tournament:tournamentList']]
        if (comment.Match.Tournament):
            menue += [[comment.Match.Tournament.Name, 'tournament:tournamentDetail', comment.Match.Tournament.id]]
        elif (comment.Match.Pool): # sometimes, comment.Match doesn't have a tournament but are in a pool belonging to a tournament
            if (comment.Match.Pool.Tournois):
                menue += [[comment.Match.Pool.Tournois.Name, 'tournament:tournamentDetail', comment.Match.Pool.Tournois.id]]
        if (comment.Match.Pool): # lors des eliminatoir, certain comment.Match n'ont pas de pool
            menue += [['pool #' + str(comment.Match.Pool.index), 'tournament:poolDetail', comment.Match.Pool.id]]
        menue += [[str(comment.Match), 'tournament:matchDetail', comment.Match.id]]
        context = {"Comment" : comment, "commentForm": commentForm, 'menue': menue}
        return render(request, template_name, context)
    else:
        form = CommentForm(request.POST)
        if (form.is_valid()):
            comment.Content = form.cleaned_data["Content"]
            comment.save()
        return HttpResponseRedirect(reverse('tournament:matchDetail',  args=[comment.Match.id]))
    
def testMap(request):
    template_name = "tournois/TestMap.html"
    context = {"longitude" : 1.433333, "lattitude" : 43.6}
    return render(request, template_name, context)

@user_passes_test(lambda u: u.is_superuser)
def editMatch(request, pk):
    if request.method == 'POST':
        if pk == 0:
            form = MatchForm(request.POST)
            if form.is_valid():
                newMatch = form.save()
                newMatch.save()
                return redirect(reverse("tournament:matchDetail", args=[newMatch.id]))
            else:
                menue = [['Accueil', 'tournament:home'], ['Liste des tournois', 'tournament:tournamentList']]
                context = {"form" : form, "id":pk, 'menue': menue}
                return render(request, template_name, context) # to change to show the issue!!!!
        else:
            match = Match.objects.get(pk=pk)
            form = MatchForm(request.POST, instance=match)
            if form.is_valid():
                form.save()
                return redirect(reverse("tournament:matchDetail", args=[pk]))
            else:
                menue = [['Accueil', 'tournament:home'], ['Liste des tournois', 'tournament:tournamentList'], [match.Tournament.Name, 'tournament:TournamentDetail', match.Tournament.id]]
                if (match.Pool): # lors des eliminatoir, certain match n'ont pas de pool
                    menue += [['pool #' + str(match.Pool.index), 'tournament:poolDetail', match.Pool.id]]
                menue += [[str(match), 'tournament:matchDetail', match.id]]
                context = {"form" : form, "id":pk, "match":match, 'menue': menue}
                return render(request, template_name, context) # to change to show the issue!!!!
    else:
        if pk == 0:
            form = MatchForm()
            match = None
        else:
            match = Match.objects.get(pk=pk)
            form = MatchForm(instance=match)
        template_name = "tournois/EditMatch.html"
        menue = [['Accueil', 'tournament:home'], ['Liste des tournois', 'tournament:tournamentList']]
        if (match):
            if (match.Tournament):
                menue += [[match.Tournament.Name, 'tournament:tournamentDetail', match.Tournament.id]]
            elif (match.Pool): # sometimes, match doesn't have a tournament but are in a pool belonging to a tournament
                if (match.Pool.Tournois):
                    menue += [[match.Pool.Tournois.Name, 'tournament:tournamentDetail', match.Pool.Tournois.id]]
            if (match.Pool): # lors des eliminatoir, certain match n'ont pas de pool
                menue += [['pool #' + str(match.Pool.index), 'tournament:poolDetail', match.Pool.id]]
            menue.append([str(match), 'tournament:matchDetail', match.id])
        context = {"form" : form, "id":pk, "match":match, 'menue': menue}
        return render(request, template_name, context)