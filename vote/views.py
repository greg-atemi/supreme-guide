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


def voter_list(request):
    return render(request, 'vote/admin/voter_list.html')


def county_list(request):
    return render(request, 'vote/admin/county_list.html')


def constituency_list(request):
    return render(request, 'vote/admin/constituency_list.html')


def ward_list(request):
    return render(request, 'vote/admin/ward_list.html')


def voter_detail(request):
    return render(request, 'vote/admin/voter_detail.html')


def county_detail(request):
    return render(request, 'vote/admin/county_detail.html')


def constituency_detail(request):
    return render(request, 'vote/admin/constituency_detail.html')


def ward_detail(request):
    return render(request, 'vote/admin/ward_detail.html')
