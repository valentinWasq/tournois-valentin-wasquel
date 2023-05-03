from django.shortcuts import render, redirect
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
        data1.append(match.Score1+match.Score2)
        data11.append(match.Encaisse1+match.Encaisse2)


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
                scoreTeam=scoreTeam+match.Score1
                scoreEncaisse=scoreEncaisse+match.Encaisse1
            if match.Team2==team:
                scoreTeam=+match.Score2
                scoreEncaisse=scoreEncaisse+match.Encaisse2
        label2.append(team.Name)
        data2.append(scoreTeam)
        data3.append({"x":scoreEncaisse,"y":scoreTeam,"r":teamsAndScores[team]})
   
    


    context=[label1,data1,data11,label2,data2,data3,label4,data4]
    #context= {"label1":label1,"data1":data1,"data11":data11, "label2":label2,"data2":data2,"label4":label4,"data4":data4}
    return context


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
    contextchart=chart(pk)
    context = {'pool': pool, 'canGenerate':canGenerate, 'label1':contextchart[0], 'data1':contextchart[1], 'data11':contextchart[2], 'label2':contextchart[3], 'data2':contextchart[4],'data3':contextchart[5], 'label4':contextchart[6],'data4':contextchart[7]}



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
                context = {"form" : form, "id":pk}
                return render(request, template_name, context) # to change to show the issue!!!!
        else:
            match = Match.objects.get(pk=pk)
            form = MatchForm(request.POST, instance=match)
            if form.is_valid():
                form.save()
                return redirect(reverse("tournament:matchDetail", args=[pk]))
            else:
                context = {"form" : form, "id":pk, "match":match}
                return render(request, template_name, context) # to change to show the issue!!!!
    else:
        if pk == 0:
            form = MatchForm()
            match = None
        else:
            match = Match.objects.get(pk=pk)
            form = MatchForm(instance=match)
        template_name = "tournois/EditMatch.html"
        context = {"form" : form, "id":pk, "match":match}
        return render(request, template_name, context)