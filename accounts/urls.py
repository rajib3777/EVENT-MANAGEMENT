from django.urls import path
from accounts.views import (
    Signupview,Signinview,Signoutview,activate_user,
    Admindashboardview,Organizerdashboardview,Participantdashboardview,
    rsvp_event,rsvp_list,Userpasswordchangeview,Userpasswordresetconfirmview,Profileview,
    Editprofileview,Userpasswordresetview
    
)

urlpatterns = [
    path('sign-up/', Signupview.as_view(), name='sign-up'),
    path('sign-in/', Signinview.as_view(), name='sign-in'),
    path('sign-out/',Signoutview.as_view(), name='logout'),
    
    path('activate/<str:uidb64>/<str:token>/',activate_user,name='activate-user'),
    
    path('admin-dashboard/',Admindashboardview.as_view(),name='admin-dashboard'),
    path('organizer-dashboard/',Organizerdashboardview.as_view(),name='organizer-dashboard'),
    path('participant-dashboard/',Participantdashboardview.as_view(),name='participant-dashboard'),
    
    path('rsvp/<int:event_id>/',rsvp_event,name='rsvp-event'),
    path('my-rsvps/',rsvp_list,name='rsvp_list'),
    
    path('Profile/', Profileview.as_view(),name='profile'),
    path('profile/edit/', Editprofileview.as_view(), name='edit-profile'),
    path('profile/change-password/', Userpasswordchangeview.as_view(), name='change-password'),
    path('reset-password/', Userpasswordresetview.as_view(),name='reset-password'),
    path('reset/<uidb64>/<token>/', Userpasswordresetconfirmview.as_view(), name='password_reset_confirm'),
]