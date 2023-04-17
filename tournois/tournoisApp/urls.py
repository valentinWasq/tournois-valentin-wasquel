from django.urls import path
from . import views

app_name = 'tournois'
urlpatterns = [
    path('', views.home, name='home')
]