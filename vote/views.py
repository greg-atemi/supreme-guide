from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'vote/index.html')


def bio(request):
    return render(request, 'vote/bio.html')


def location(request):
    return render(request, 'vote/location.html')


def photo(request):
    return render(request, 'vote/photo.html')


def success(request):
    return render(request, 'vote/success.html')

