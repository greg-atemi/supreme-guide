from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'vote/user/index.html')


def bio(request):
    return render(request, 'vote/user/bio.html')


def location(request):
    return render(request, 'vote/user/location.html')


def photo(request):
    return render(request, 'vote/user/photo.html')


def success(request):
    return render(request, 'vote/user/success.html')


def confirm(request):
    return render(request, 'vote/user/confirmation.html')


def admin(request):
    return render(request, 'vote/admin/admin_base.html')
