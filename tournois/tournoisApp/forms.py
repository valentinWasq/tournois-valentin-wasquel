from django import forms
from django.forms import ModelForm
from .models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['Content']
        
class SearchForm(forms.Form):
    query = forms.CharField(max_length=150, label="Team(s), date, score of a match")