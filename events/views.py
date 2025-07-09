from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from .models import Event,Participant,Category
from .forms import EventForm,ParticipantForm,CategoryForm
from django.utils.text import slugify
from django.db.models import Sum




#---- Homepage ----#

def home(request):
    today = timezone.now().date()
    previous_events = Event.objects.filter(date__lt=today).select_related('category')
    todays_events = Event.objects.filter(date=today).select_related('category')
    upcoming_events =  Event.objects.filter(date__gt=today).select_related('category')


    context = {
        'previous_events' : previous_events,
        'todays_events' : todays_events,
        'upcoming_events' : upcoming_events,
    }
    
    return render(request,'home.html',context)


#---- dashboard ----#

def dashboard(request):
    today = timezone.now().date()
    total_participants = Participant.objects.count()
    total_events = Event.objects.count()
    previous_events = Event.objects.filter(date__lt=today).select_related('category')
    todays_events = Event.objects.filter(date=today).select_related('category')
    upcoming_events =  Event.objects.filter(date__gt=today).select_related('category')
    total_participants = Participant.objects.count()
    


    context = {
        'total_events' : total_events,
        'total_participants' : total_participants,
        'previous_events' : previous_events,
        'todays_events' : todays_events,
        'upcoming_events' : upcoming_events,
    }
    
    return render(request,'dashboard.html',context)

#---- Event_details ----#

def event_detail(request,pk):
    event = get_object_or_404(
        Event.objects.select_related('category').prefetch_related('participants'),
        pk=pk
    )
    
    return render(request,'events/event_detail.html',{'event' : event})

    
#---- Event_crud ----#
def event_list(request):
    query = request.GET.get('q')
    today = timezone.now().date()
    events = Event.objects.filter(status='published').select_related('category').order_by('date')
    
    category_id = request.GET.get('category')
    
    if category_id:
        events = events.filter(category_id=category_id)
        
    if query :
        from django.db.models import Q
        events = events.filter(
            Q(name__icontains = query) | Q(location__icontains = query)
        )
    
    image_list = [
        'christmas-market-4705877_1920.jpg',
        'recall.avif',
        'home.jpg',
        'OIP_2.webp',
    ] 
        
    context = {
        'events' : events,
        'categories' : Category.objects.all(),
        'selected_category' : int (category_id) if category_id else None,
        'image_list': image_list
        
    }    
    
    return render(request,'events/event_list.html',context)
    

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST,request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.slug = slugify(event.name)
            event.status = 'published'
            event.save()
            form.save_m2m()
            return redirect('event_list')
    else:
        form = EventForm()
        
    return render(request,'events/event_form.html',{'form':form})


def event_update(request,pk):
    event = get_object_or_404(Event,pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST,request.FILES,instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
        
        
    else:
        form = EventForm(instance=event)
        
    return render(request,'events/event_form.html',{'form':form})



def event_delete(request,pk):
    event = get_object_or_404(Event,pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
        
    return render(request,'events/event_confirm_delete.html',{'event':event})



#---- category crud ----#

def category_list(request):
    categories = Category.objects.all()
    return render(request,'category/category_list.html',{'categories' : categories})


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category_list')
        
        
    else:
        form = CategoryForm()
        
    return render(request,'category/category_form.html',{'form':form})

def category_update(request,pk):
    category = get_object_or_404(Category,pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST,request.FILES,instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
        
        
    else:
        form = CategoryForm(instance=category)
        
    return render(request,'category/category_form.html',{'form':form})


    
def category_delete(request,pk):
    category = get_object_or_404(Category,pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
        
    return render(request,'category/category_delete.html',{'category':category})

#---- participant crud ----#

def participant_list(request):
    participant = Participant.objects.all()
    return render(request,'participants/participant_list.html',{'participants' : participant})



def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
        
        
    else:
        form = ParticipantForm()
        
    return render(request,'participants/participant_form.html',{'form':form})

def participant_update(request,pk):
    participant = get_object_or_404(Participant,pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST,request.FILES,instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
        
        
    else:
        form = ParticipantForm(instance=participant)
        
    return render(request,'participants/participant_form.html',{'form':form})


    
def participant_delete(request,pk):
    participant = get_object_or_404(Participant,pk=pk)
    if request.method == 'POST':
        participant.delete()
        return redirect('participant_list')
        
    return render(request,'participants/participant_delete.html',{'participant':participant})

def about_view(request):
    return render(request, 'about.html')


def gallery_view(request):
    return render(request, 'gallery.html')