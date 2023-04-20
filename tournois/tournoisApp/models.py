from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Team(models.Model):
    Name = models.CharField(max_length=50)
    Coach = models.CharField(max_length=50)
    ListOfPLayer = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.Name} : coach: {self.Coach}; players: {self.ListOfPLayer}"
    
    def getMatch(self):
        return self.Matchs_team1.all() + self.Matchs_team2.all()
    
    def getScore(self):
        score = 0
        for match in self.Matchs_team1.all():
            score += match.Score1
        for match in self.Matchs_team2.all():
            score += match.Score1
        return score
        
class Tournament(models.Model):
    Name = models.CharField(max_length=50)
    Location = models.CharField(max_length=50, null=True)
    Dates = models.CharField(max_length=200, null=True)
    NBPool = models.IntegerField(default=0)
    NBTeamPerPool = models.IntegerField(default = 0)

class Pool(models.Model):
    Tournois = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING)
    index = models.IntegerField(default=-1)
    
    def getTeams(self):
        AllMatch = self.match_set.all()
        AllTeams = []
        for match in AllMatch:
            for team in match.Teams():
                if (team not in AllTeams):
                    AllTeams += [team]
        return AllTeams


class Match(models.Model):
    Date = models.DateField()
    Location = models.CharField(max_length=50)
    Team1 = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="Matchs_team1")
    Team2 = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="Matchs_team2")
    Score1 = models.IntegerField(default=0)
    Score2 = models.IntegerField(default=0)
    Pool = models.ForeignKey(Pool, on_delete=models.DO_NOTHING)

    def getScoreString(self):
        return str(self.Score1) + ':' + str(self.Score2)
    
    def Teams(self):
        return [self.Team1, self.Team2]
    
    def Scores(self):
        return [self.Score1, self.Score2]

    def __str__(self):
        return f"match {self.Team1.Name} against {self.Team2.Name}, score : {self.getScoreString()} \nat : {self.Location}, {self.Date}"

class Comment(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Match = models.ForeignKey(Match, on_delete=models.CASCADE)
    Date = models.DateField()
    Content = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.User.username} : {self.Content} (time : {self.Date})"