from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('participantsignup/', views.participantsignup, name='participantsignup'),
    path('login/', views.login, name='login'),
    path('signupportal/', views.signupportal, name='signupportal'),
    path('partdas/', views.partdas, name='partdas'),
    path('jointeam/<int:id>/', views.jointeam, name='jointeam'),
    path('createteam/<int:id>/', views.createteam, name='createteam'),
    path('hostsignup/', views.hostsignup, name='hostsignup'),
    path('otp/', views.otp, name='otp'),
    path('hostdash/', views.hostdash, name='hostdash'),
    path('eventwise/<int:id>/',views.eventwise, name='eventwise'),

]