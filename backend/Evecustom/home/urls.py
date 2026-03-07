from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('participantsignup/', views.participantsignup, name='participantsignup'),
    path('partdas/', views.partdas, name='partdas'),
   path('jointeam/', views.jointeam, name='jointeam'),
   path('createteam/', views.createteam, name='createteam'),
]