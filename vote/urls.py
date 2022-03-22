from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

app_name = 'vote'

urlpatterns = [
    path('', views.index, name='index'),
    path('bio', views.bio, name='bio'),
    path('location', views.location, name='location'),
    path('photo', views.photo, name='photo'),
    path('success', views.success, name='success'),
    path('confirmation', views.confirmation, name='confirmation'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('voter_list', views.voter_list, name='voter_list'),
    path('create_voter', views.create_voter, name='create_voter'),
    path('county_list', views.county_list, name='county_list'),
    path('county_detail', views.county_detail, name='county_detail'),
    path('ward_list', views.ward_list, name='ward_list'),
    path('ward_detail', views.ward_detail, name='ward_detail'),
    path('constituency_list', views.constituency_list, name='constituency_list'),
    path('constituency_detail', views.constituency_detail, name='constituency_detail'),
    path('auth', views.auth, name='auth'),
    path('auth2', views.auth2, name='auth2'),
    path('auth3', views.auth3, name='auth3'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('admin_account', views.admin_account, name='admin_account'),
    path('log_out', views.log_out, name='log_out'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('activation_failed', views.activation_failed, name='activation_failed')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
