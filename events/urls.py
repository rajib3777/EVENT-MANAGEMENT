from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import about_view


urlpatterns = [
    path('gallery/', views.gallery_view, name='gallery'),
    path('about/', about_view, name='about'),
    #event-crud
    path('',views.home,name='home'),
    path('events/',views.event_list,name='event_list'),
    path('events/<int:pk>/',views.event_detail,name='event_detail'),
    path('events/create/',views.event_create,name='event_create'),
    path('events/<int:pk>/update/',views.event_update,name='event_update'),
    path('events/<int:pk>/delete/',views.event_delete,name='event_delete'),
    
    
    #participant-crud
    path('participants/',views.participant_list,name='participant_list'),
    path('participants/create/',views.participant_create,name='participant_create'),
    path('participants/<int:pk>/update/',views.participant_update,name='participant_update'),
    path('participants/<int:pk>/delete/',views.participant_delete,name='participant_delete'),
    
    # categories
    
    path('categories/',views.category_list,name='category_list'),
    path('categories/create/',views.category_create,name='category_create'),
    path('categories/<int:pk>/update/',views.category_update,name='category_update'),
    path('categories/<int:pk>/delete/',views.category_delete,name='category_delete'),
    
    #dashboard
    
    path('dashboard/',views.dashboard,name='dashboard'),

]



#thumb--->
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


