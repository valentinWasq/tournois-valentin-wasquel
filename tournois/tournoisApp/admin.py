from django.contrib import admin

# Register your models here.
from .models import Tournament, Pool, Match, Team, Comment

admin.site.register(Tournament)
admin.site.register(Pool)
admin.site.register(Match)
admin.site.register(Team)
admin.site.register(Comment)
