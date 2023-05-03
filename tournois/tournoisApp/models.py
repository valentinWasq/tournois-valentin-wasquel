from django.db import models
from django.contrib.auth.models import User
from random import randint
import math

# Create your models here.
class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

class Team(models.Model):
    Name = models.CharField(max_length=50)
    Coach = models.CharField(max_length=50)
    ListOfPLayer = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.Name} : coach: {self.Coach}; players: {self.ListOfPLayer}"
    
    #because the team can be in team1 or 2, this function return all the pool the team is regardless of what team it is
    def getMatch(self):
        return self.Matchs_team1.all() + self.Matchs_team2.all()
    

    def getScore(self):
        score = 0
        for match in self.Matchs_team1.all():
            if match.Score1 != None:
                score += match.Score1
        for match in self.Matchs_team2.all():
            if match.Score2 != None:
                score += match.Score2
        return score
        
class Tournament(models.Model):
    Name = models.CharField(max_length=50)
    Location = models.CharField(max_length=50, null=True)
    Date = models.DateField(null=True)
    End_date = models.DateField(null = True, blank=True)
    NBPool = models.IntegerField(default=0)
    NBTeamPerPool = models.IntegerField(default = 0)
    # added theses field so different tournament can have different counting system
    NBPointOnWin = models.IntegerField(default=3)
    NBPointOnTie = models.IntegerField(default=1)
    NBPointOnLose = models.IntegerField(default=0)
    
    def __str__(self):
        return self.Name
    
    """
        Generate the next round of the knockout phase of a tournament given its rank
        For instance in a tournament with 16 teams out of the pool generateNextRound(2)
        will create matches for the quarterfinale (pool=0; 8th fo finale=1; quarterfinale=2; halffinale=3; finale=4)
    """
    def generateNextRound(self, round):
        matchList = []

        if round < 1 or round > math.log2(2*self.NBPool):
                print("Incorrect number of round")

        # Generate the first round after the pool phase
        elif round == 1 :
            for i in range(self.NBPool)[::2]:
                # ith pool
                pool1 = self.pool_set.all()[i]
                if len(pool1.match_set.all()) < self.NBTeamPerPool * (self.NBTeamPerPool-1)/2:
                    pool1.createAllMatch()

                # i+1th pool
                pool2 = self.pool_set.all()[i+1]
                if len(pool2.match_set.all()) < self.NBTeamPerPool * (self.NBTeamPerPool-1)/2:
                    pool2.createAllMatch()

                # First team of the ith pool
                team1 = list(pool1.getTeamsAndScores().items())[0][0]
                # Second team of he i+1th pool
                team2 = list(pool2.getTeamsAndScores().items())[1][0]
                # First team of he i+1th pool
                team3 = list(pool2.getTeamsAndScores().items())[0][0]
                # Second team of he ith pool
                team4 = list(pool1.getTeamsAndScores().items())[1][0]
                
                match1 = Match(Date=None, Location=self.Location, Team1=team1, Team2=team2, isPool=False, Tournament=self, Round=round)
                match1.save()

                match2 = Match(Date=None, Location=self.Location, Team1=team3, Team2=team4, isPool=False, Tournament=self, Round=round)
                match2.save()
        
        # Generate next round after a knockout round
        elif round > 1 and round <= math.log2(2*self.NBPool):
            lastRoundMatches = Match.objects.filter(Tournament=self).filter(isPool=False).filter(Round=round-1)
            for i in range(len(lastRoundMatches))[::2]:

                # If the two previous matches were played
                if lastRoundMatches[i].getWinner() != None and lastRoundMatches[i+1].getWinner() != None:
                    winner1 = lastRoundMatches[i].getWinner()
                    winner2 = lastRoundMatches[i+1].getWinner()
                    match = Match(Date=None, Location=self.Location, Team1=winner1, Team2=winner2, isPool=False, Tournament=self, Round=round)
                    match.save()

    

    """
        Generate random results for the knockout phase matches (designed to be used only in developpment)
    """
    def randomScores(self):
        for match in self.match_set.all():
            if match.Score1 == None:
                match.Score1 = randint(0,6)
            if match.Score2 == None:
                match.Score2 = randint(0,6)
            match.save()

                    

    """
        Delete all the matches from the knockout phase of this tournament
    """
    def cleanKnockoutMatches(self):
        for match in Match.objects.filter(Tournament=self).filter(isPool=False):
            match.delete()

    """
        Return only the matches in the knockout phase
    """
    def filterKnockoutMatches(self, round=None):
        if round == None:
            return Match.objects.filter(Tournament=self).filter(isPool=False)
        else:
            return Match.objects.filter(Tournament=self).filter(isPool=False).filter(Round=round)
    
    """
        Return a list of query each containing the matches having the index
        as their round number
    """
    def matchesSortedbyRound(self):
        rounds = []
        for i in range (1,int(math.log2(2*self.NBPool)+1)):
            rounds.append(self.filterKnockoutMatches(i))
        return rounds



class Pool(models.Model):
    Tournois = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING)
    index = models.IntegerField(default=-1)
    Teams = models.ManyToManyField(Team)
    
    def __str__(self):
        return "Poule " + str(self.index)
    
    #return a sorted dictionary of all the teams in this pool and they score
    def getTeamsAndScores(self):
        Result = {}
        tournament = self.Tournois #store the tournament here as it will be called repepetatively
        for match in self.match_set.all():
            if match.Score1!=None and match.Score2!=None:
                if match.Score1 > match.Score2:
                    Score1 = tournament.NBPointOnWin
                    Score2 = tournament.NBPointOnLose
                elif match.Score1 < match.Score2:
                    Score2 = tournament.NBPointOnWin
                    Score1 = tournament.NBPointOnLose
                else:
                    Score2 = tournament.NBPointOnTie
                    Score1 = tournament.NBPointOnTie
            
            else:
                Score1 = 0
                Score2 = 0
            if match.Team1 in Result:
                Result[match.Team1] += Score1
            else:
                Result[match.Team1] = Score1
            if match.Team2 in Result:
                Result[match.Team2] += Score2
            else:
                Result[match.Team2] = Score2
        orderedResult = {k: v for k, v in sorted(Result.items(), key=lambda item: -item[1])}
        return orderedResult
    
    # Deletes all the matches of this pool in the database
    def cleanMatches(self):
        for match in self.match_set.all():
            match.delete()
    
    def createAllMatch(self):
        tournament = self.Tournois
        allTeam = self.Teams.all()
        if len(allTeam) < tournament.NBTeamPerPool: # check if we have the correct amount of teams
            return
        listOfAllRencontre = []
        # double loop to create all the pairs of team possible
        for i in range(len(allTeam)):
            for j in range(i+1, len(allTeam)):
                listOfAllRencontre += [(allTeam[i], allTeam[j])]
        for team1, team2 in listOfAllRencontre: # create all the matches
            match = Match(Date=None, Location=tournament.Location, Team1=team1, Team2=team2, Pool=self)
            match.save()

    # Generate random results for the matches in this pool(designed to be used only in developpment)
    def randomScores(self):
        for match in self.match_set.all():
            if match.Score1 == None:
                match.Score1 = randint(0,6)
            if match.Score2 == None:
                match.Score2 = randint(0,6)
            match.save()



class Match(models.Model):
    Date = models.DateTimeField(null=True)
    Location = models.CharField(max_length=50)
    # GPS location of the match, will be set in a new view
    Longitude = models.FloatField(null=True)
    Lattitude = models.FloatField(null=True)
    Team1 = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="Matchs_team1")
    Team2 = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="Matchs_team2")
    Score1 = models.IntegerField(null=True, blank=True)
    Score2 = models.IntegerField(null=True, blank=True)
    isPool = models.BooleanField(default=True, blank=True)
    Round = models.IntegerField(default=0, blank=True)
    Pool = models.ForeignKey(Pool, null=True, on_delete=models.DO_NOTHING)
    Tournament = models.ForeignKey(Tournament, null=True, on_delete=models.DO_NOTHING)


    def getScoreString(self):
        return str(self.Score1) + ':' + str(self.Score2)
       
    
    def Teams(self):
        return [self.Team1, self.Team2]
    
    def Scores(self):
        return [self.Score1, self.Score2]
    
    """
        Return the winner of a match
        Should only be used in the knockout phase since it can't deal with draw
    """
    def getWinner(self):
        if self.Score1==None or self.Score2==None:
            return None
        elif self.Score1 > self.Score2:
            return self.Team1
        elif self.Score2 > self.Score1:
            return self.Team2
        else:
            return self.Team1 if randint(0,1) else self.Team2

    def __str__(self):
        if self.Score1!=None and self.Score2!=None:
            return f"match {self.Team1.Name} against {self.Team2.Name}, score : {self.getScoreString()} \nat : {self.Location}, {self.Date}"
        else:
            return f"match {self.Team1.Name} against {self.Team2.Name}, \nat : {self.Location}, {self.Date}"

class Comment(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Match = models.ForeignKey(Match, on_delete=models.CASCADE)
    Date = models.DateField()
    Content = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.User.username} : {self.Content} (time : {self.Date})"