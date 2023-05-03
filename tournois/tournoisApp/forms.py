from django import forms
from django.forms import ModelForm, Textarea
from .models import Comment, Match

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['Content']
        widgets = {
            "content": Textarea(attrs={"cols": 80, "rows": 3}),
        }
        
class SearchForm(forms.Form):
    query = forms.CharField(max_length=150, label="Recherche")
    widgets = {
            "content": Textarea(attrs={"cols": 80, "rows": 1}),
        }

class MatchForm(ModelForm):
    class Meta:
        model = Match
        fields = '__all__'