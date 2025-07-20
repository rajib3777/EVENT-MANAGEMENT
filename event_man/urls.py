from django.contrib import admin
from django.urls import path,include
from accounts.views import sign_up
from django.shortcuts import redirect

# def redirect_to_signup(request):
#     return redirect('sign-up')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', sign_up, name='root-sign-up'),
    path('accounts/', include('accounts.urls')),
    path('',include('events.urls')),
]



