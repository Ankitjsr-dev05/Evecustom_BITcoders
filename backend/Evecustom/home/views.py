from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def participantsignup(request):
    return render(request, 'participantsignup.html')
def partdas(request):
    return render(request, 'partdas.html')