from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html', {'name': 'Camilo Arbelaez'})

def about(request):
    return HttpResponse("About Page")




