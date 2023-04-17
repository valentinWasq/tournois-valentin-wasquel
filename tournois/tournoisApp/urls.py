from django.urls import path
import views

app_name = 'tournois'
urlpatterns:[
    path('', veiws.home, name='home')
]