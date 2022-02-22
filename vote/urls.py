from django.urls import path

from . import views

app_name = 'vote'

urlpatterns = [
    path('bio', views.bio, name='bio'),
    path('location', views.location, name='location'),
    path('photo', views.photo, name='photo'),
    path('success', views.success, name='success'),
    path('confirm', views.confirm, name='confirm'),
    path('voter_list', views.voter_list, name='voter_list'),
    path('voter_detail', views.voter_detail, name='voter_detail'),
    path('county_list', views.county_list, name='county_list'),
    path('county_detail', views.county_detail, name='county_detail'),
    path('ward_list', views.ward_list, name='ward_list'),
    path('ward_detail', views.ward_detail, name='ward_detail'),
    path('constituency_list', views.constituency_list, name='constituency_list'),
    path('constituency_detail', views.constituency_detail, name='constituency_detail'),
]
