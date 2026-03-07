from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('participantsignup/', views.participantsignup, name='participantsignup'),
    path('hostlogin/', views.hostlogin, name='hostlogin'),
    path('signupportal/', views.signupportal, name='signupportal'),

]