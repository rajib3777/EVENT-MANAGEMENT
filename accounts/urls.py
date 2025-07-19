from django.urls import path
from accounts.views import (
    sign_up, sign_in, sign_out,activate_user,
    admin_dashboard,organizer_dashboard,participant_dashboard,
    rsvp_event,rsvp_list
)

urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', sign_out, name='logout'),
    
    path('activate/<str:uidb64>/<str:token>/',activate_user,name='activate-user'),
    
    path('admin-dashboard/',admin_dashboard,name='admin-dashboard'),
    path('organizer-dashboard/',organizer_dashboard,name='organizer-dashboard'),
    path('participant-dashboard/',participant_dashboard,name='participant-dashboard'),
    
    path('rsvp/<int:event_id>/',rsvp_event,name='rsvp-event'),
    path('my-rsvps/',rsvp_list,name='rsvp_list'),
]