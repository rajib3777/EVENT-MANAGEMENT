from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from django.contrib.auth import login, authenticate, logout
from accounts.forms import CustomRegistrationForm #,LoginForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.forms import AuthenticationForm as LoginForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.db.models import Count
from events.models import Event




from events.models import Event
# Create your views here.


def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False   
            user.save()
                     
            role = form.cleaned_data.get('role')
            
            if role == 'Organizer':
                group, _ = Group.objects.get_or_create(name='Organizer')
            else:
                group, _ = Group.objects.get_or_create(name='Participant')
                
                
            user.groups.add(group)
                

            #token
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            #activation_link
            
            activation_link = request.build_absolute_uri(
                reverse_lazy('activate-user', kwargs={'uidb64':uid,'token':token})
            )
            
            

            
            #actiavtion mail
            subject = 'Activate your account'
            message = render_to_string('accounts/activation_mail.html',{
                'user' : user,
                'activation_link' : activation_link,
            })
            
            email = EmailMultiAlternatives(subject,'',to=[user.email])
            email.attach_alternative(message,'text/html')
            email.send()
                        
            messages.success(
                request, 'A Confirmation mail sent. Please check your email')
            return redirect('sign-in')

        else:
            print("Form is not valid")
    return render(request, 'accounts/register.html', {"form": form})


def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if user.is_superuser:
                return redirect('admin-dashboard')
            elif user.groups.filter(name='Organizer').exists():
                return redirect('organizer-dashboard')
            else:
                return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')


def activate_user(request, uidb64 , token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')
    
# @login_required
# @user_passes_test(lambda u: u.is_superuser)
# def admin_dashboard(request):
#     return render(request,'accounts/admin_dashboard.html')
def admin_dashboard(request):
    events = Event.objects.all()
    today = timezone.now().date()
    total_events = events.count()
    past_events = events.filter(date__lt=today)
    upcoming_events = events.filter(date__gte=today)
    total_upcoming = upcoming_events.count()
    
    total_rsvp_count = sum(event.rsvps.count() for event in events)


    context = {
        'events' : events,
        'total_events' :total_events,
        'upcoming_events' : upcoming_events,
        'past_events' : past_events,
        'total_rsvp_count' : total_rsvp_count,
        'total_upcoming' : total_upcoming,
        
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Organizer').exists())
def organizer_dashboard(request):
    return render(request,'accounts/organizer_dashboard.html')


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Participant').exists())
def participant_dashboard(request):
    return render(request,'accounts/participant_dashboard.html')


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Participant').exists())
def rsvp_event(request,event_id):
    event = get_object_or_404(Event,id=event_id)
    if request.user in event.rsvps.all():
        messages.info(request,"You already RSVP'd for this event.")
    else:
        event.rsvps.add(request.user)
        messages.success(request,"RSVP successful! Check your email for confirmation.")  
    return redirect('participant-dashboard')


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Participant').exists())
def rsvp_list(request):
    events = request.user.event_rsvps.all()
    return render(request,'accounts/rsvp_list.html',{'events':events})


admin_dashboard