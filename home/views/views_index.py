from django.shortcuts import render

def index(request):
    return render(request, 'plantaopro/pages/index.html')
