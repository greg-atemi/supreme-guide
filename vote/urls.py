from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

app_name = 'vote'

urlpatterns = [
    path('', views.index, name='index'),
    path('bio', views.bio, name='bio'),
    path('location/<str:id_serial_number>/', views.location, name='location'),
    path('photo/<str:id_serial_number>/', views.photo, name='photo'),
    path('confirmation/<str:id_serial_number>/', views.confirmation, name='confirmation'),
    path('success', views.success, name='success'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('voter_list', views.voter_list, name='voter_list'),
    path('create_voter', views.create_voter, name='create_voter'),
    path('county_list', views.county_list, name='county_list'),
    path('county_detail', views.county_detail, name='county_detail'),
    path('update_county/<str:county_code>/', views.update_county, name='update_county'),
    path('delete_county/<str:county_code>/', views.delete_county, name='delete_county'),
    path('ward_list', views.ward_list, name='ward_list'),
    path('ward_detail', views.ward_detail, name='ward_detail'),
    path('update_ward/<str:ward_code>/', views.update_ward, name='update_ward'),
    path('delete_ward/<str:ward_code>/', views.delete_ward, name='delete_ward'),
    path('constituency_list', views.constituency_list, name='constituency_list'),
    path('constituency_detail', views.constituency_detail, name='constituency_detail'),
    path('update_constituency/<str:constituency_code>/', views.update_constituency, name='update_constituency'),
    path('delete_constituency/<str:constituency_code>/', views.delete_constituency, name='delete_constituency'),
    path('check_details_auth', views.check_details_auth, name='check_details_auth'),
    path('update_details_auth', views.update_details_auth, name='update_details_auth'),
    # path('voter_details', views.voter_details, name='voter_details'),
    path('voter_details/<str:id_serial_number>/', views.voter_details, name='voter_details'),
    path('update_details/<str:id_serial_number>/', views.update_details, name='update_details'),
    path('auth2', views.auth2, name='auth2'),
    path('auth3', views.auth3, name='auth3'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('user_account', views.user_account, name='user_account'),
    path('admin_account', views.admin_account, name='admin_account'),
    path('log_out', views.log_out, name='log_out'),
    path('admin_log_out', views.admin_log_out, name='admin_log_out'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('activation_failed', views.activation_failed, name='activation_failed')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
