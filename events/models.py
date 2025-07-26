from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model

      
# Create your models here.
User = get_user_model()
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = CloudinaryField(
    'image',
    blank=True,
    null=True
    )

    def __str__(self):
        return self.name


class Event(models.Model):
    
    STATUS_CHOICES= [
        ('draft','Draft'),
        ('published','Published'),
        ('canceled','Canceled'),
    ]
    # participants
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    
    
    rsvps = models.ManyToManyField(User, related_name='event_rsvps', blank=True)
    
    max_seats = models.PositiveBigIntegerField(default=0)
    
    
    
    category=models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # participants = models.ManyToManyField('Participant',blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    
    thumbnail = CloudinaryField(
        'image',
        blank=True,
        null=True
    )
    
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            counter = 1
            while Event.objects.filter(slug = self.slug).exists():
                self.slug = f"{slugify(self.name)}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return self.name 
    
    



