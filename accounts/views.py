from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from accounts.forms import CustomRegistrationForm #,LoginForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.forms import AuthenticationForm as LoginForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.db.models import Count
from .models import Customuser
from django.views.generic import View
from events.models import Event
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView,UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import Profileupdateform
from django.contrib.auth.views import PasswordChangeView,PasswordResetView,PasswordResetConfirmView
# Create your views here.


class Signupview(View):
    def get(self, request):
        form = CustomRegistrationForm()
        return render(request, 'accounts/register.html', {"form": form})
    
    def post(self, request):
        form = CustomRegistrationForm(request.POST)
        print("✅ Form validity:", form.is_valid())
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
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))        
            activation_link = request.build_absolute_uri(
                reverse_lazy('activate-user', kwargs={'uidb64':uid,'token':token})
            )
            
            subject = 'Activate your account'
            message = render_to_string('accounts/activation_mail.html',{
                'user' : user,
                'activation_link' : activation_link,
            })
            
            # email = EmailMultiAlternatives(subject,'',to=[user.email])
            # email.attach_alternative(message,'text/html')
            # email.send()
            # print("✅ Activation email sent to:", user.email)
            try:
                activation_email = EmailMultiAlternatives(subject, '', to=[user.email])
                activation_email.attach_alternative(message, 'text/html')
                activation_email.send()
                print("✅ Email sent")
            except Exception as e:
                print("❌ Email error:", e)


                        
            messages.success(request, 'A Confirmation mail sent. Please check your email')
            return redirect('sign-in')
        
        return render(request, 'accounts/register.html', {"form": form})

# def sign_up(request):
#     form = CustomRegistrationForm()
#     if request.method == 'POST':
#         print("📥 Received POST request for signup")
#         form = CustomRegistrationForm(request.POST)
#         print("✅ Form validity:", form.is_valid())
#         if form.is_valid():
#             try:
#                 email.send()
#                 print("✅ Email sent")
#             except Exception as e:
#                 print("❌ Email error:", e)
                
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data.get('password1'))
#             user.is_active = False   
#             user.save()
                     
#             role = form.cleaned_data.get('role')
            
#             if role == 'Organizer':
#                 group, _ = Group.objects.get_or_create(name='Organizer')
#             else:
#                 group, _ = Group.objects.get_or_create(name='Participant')
                
                
#             user.groups.add(group)
                

#             #token
            
#             token = default_token_generator.make_token(user)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
            
#             #activation_link
            
#             activation_link = request.build_absolute_uri(
#                 reverse_lazy('activate-user', kwargs={'uidb64':uid,'token':token})
#             )
            
            

            
#             #actiavtion mail
#             subject = 'Activate your account'
#             message = render_to_string('accounts/activation_mail.html',{
#                 'user' : user,
#                 'activation_link' : activation_link,
#             })
            
#             email = EmailMultiAlternatives(subject,'',to=[user.email])
#             email.attach_alternative(message,'text/html')
#             email.send()
#             email.send()
#             print("✅ Activation email sent to:", user.email)

                        
#             messages.success(
#                 request, 'A Confirmation mail sent. Please check your email')
#             return redirect('sign-in')

#         else:
#             print("Form is not valid")
           
#             print("❌ Form invalid:", form.errors)

#     return render(request, 'accounts/register.html', {"form": form})
class Signinview(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        
        if user.is_superuser:
            return reverse_lazy('admin-dashboard')
        elif user.groups.filter(name='Organizer').exists():
            return reverse_lazy('organizer-dashboard')
        else:
            return reverse_lazy('participant-dashboard')

# def sign_in(request):
#     form = LoginForm()
#     if request.method == 'POST':
#         form = LoginForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
            
#             if user.is_superuser:
#                 return redirect('admin-dashboard')
#             elif user.groups.filter(name='Organizer').exists():
#                 return redirect('organizer-dashboard')
#             else:
#                 return redirect('home')
#     return render(request, 'accounts/login.html', {'form': form})


    
class Signoutview(LogoutView):
    next_page = reverse_lazy('sign-in')
# @login_required
# def sign_out(request):
#     if request.method == 'POST':
#         logout(request)
#         return redirect('sign-in')


def activate_user(request, uidb64 , token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        User = get_user_model()
        user = User.objects.get(id=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')
    
class Admindashboardview(TemplateView):
    template_name = 'accounts/admin_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = Event.objects.all()
        today = timezone.now().date()
        context['events'] = events
        context['total_events'] = events.count()
        context['past_events'] = events.filter(date__lt=today)
        context['upcoming_events'] = events.filter(date__gte=today)
        context['total_upcoming'] = context['upcoming_events'].count()
        context['total_rsvp_count'] = sum(event.rsvps.count() for event in events)
        return context

# def admin_dashboard(request):
#     events = Event.objects.all()
#     today = timezone.now().date()
#     total_events = events.count()
#     past_events = events.filter(date__lt=today)
#     upcoming_events = events.filter(date__gte=today)
#     total_upcoming = upcoming_events.count()
    
#     total_rsvp_count = sum(event.rsvps.count() for event in events)


#     context = {
#         'events' : events,
#         'total_events' :total_events,
#         'upcoming_events' : upcoming_events,
#         'past_events' : past_events,
#         'total_rsvp_count' : total_rsvp_count,
#         'total_upcoming' : total_upcoming,
        
#     }
#     return render(request, 'accounts/admin_dashboard.html', context)


# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='Organizer').exists())
# def organizer_dashboard(request):
#     return render(request,'accounts/organizer_dashboard.html')


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



class Organizerdashboardview(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'accounts/organizer_dashboard.html'
    
    def test_func(self):
        return self.request.user.groups.filter(name='Organizer').exists()
    
class Participantdashboardview(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'accounts/participant_dashboard.html'
    
    def test_func(self):
        return self.request.user.groups.filter(name='Participant').exists()
    

class Profileview(LoginRequiredMixin,DetailView):
    model = Customuser
    template_name = 'accounts/profile.html'
    
    def get_object(self):
        return self.request.user
    
class Editprofileview(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Customuser
    form_class = Profileupdateform
    template_name = 'accounts/edit_profile.html' 
    success_url = reverse_lazy('profile')
    success_message = "Profile update Successfully"
    
    def get_object(self):
        return self.request.user
    
class Userpasswordchangeview(LoginRequiredMixin,SuccessMessageMixin,PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('profile')
    success_message = "Password reset email sent.Check your inbox"
    
class Userpasswordresetview(SuccessMessageMixin,PasswordResetView):
    template_name = 'accounts/reset_password.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('sign-in')
    success_message = "Password reset mail sent. check your inbox"
    
class Userpasswordresetconfirmview(SuccessMessageMixin,PasswordResetConfirmView):
    template_name = 'accounts/reset_confirm.html'
    success_url = reverse_lazy('sign-in')
    success_message = "Password reset successfully.You can now log in."
        