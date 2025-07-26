from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

def user_directory_path(instance, filename):
    return f'user_{instance.id}/{filename}'

class Customuser(AbstractUser):
    ROLE_CHOICES = (
        ('Participant','Participant'),
        ('Organizer','Organizer'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')
    mobile_number = models.CharField(max_length=15,blank=True)
    profile_picture = models.ImageField(upload_to=user_directory_path,default='default.jpg')
    
    def __str__(self):
        return self.username

