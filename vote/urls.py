from django.urls import path

from . import views

app_name = 'vote'

urlpatterns = [
    path('bio', views.bio, name='bio'),
    path('location', views.location, name='location'),
    path('photo', views.photo, name='photo'),
    path('success', views.success, name='success'),
]
