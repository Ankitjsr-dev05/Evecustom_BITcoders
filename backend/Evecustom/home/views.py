from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def participantsignup(request):
    return render(request, 'participantsignup.html')
def partdas(request):
    return render(request, 'partdas.html')
def jointeam(request):
    return render(request, 'jointeam.html')
def createteam(request):
    return render(request, 'createteam.html')
def aboutus(request):
    return render(request, 'aboutus.html')
def achie(request):
    return render(request, 'achie.html')