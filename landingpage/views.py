from django.shortcuts import render

def home(request):
    return render(request, 'landingpage/home.html')

def terms(request):
    return render(request, 'landingpage/terms.html')

def privacy(request):
    return render(request, 'landingpage/privacy.html')
