from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def participantsignup(request):
    return render(request, 'participantsignup.html')

def hostlogin(request):
    return render(request, 'hostlogin.html') 

def signupportal(request):
    return render(request, 'signupportal.html')

def hostsignup(request):
    return render(request, 'hostsignup.html')