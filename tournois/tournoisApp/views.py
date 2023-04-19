from django.shortcuts import render

from .models import Tournament, Pool

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
    context = {'pool': pool}
    return render(request, template_name, context)