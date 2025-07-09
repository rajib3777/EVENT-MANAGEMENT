from django import forms
from .models import Event,Participant,Category
from django.forms import DateTimeInput,DateInput,TimeInput


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['slug','created_at','updated_at']
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'date' : DateInput(attrs={'type' : 'date','class':'form-control'}),
            'time' : TimeInput(attrs={'type' : 'time','class':'form-control'}),
            'description' : forms.Textarea(attrs={'rows' : 4,'class':'form-control'}),
            'category' : forms.Select(attrs={'rows':'form-select'}),
            'participants' : forms.SelectMultiple(attrs={'class':'form-select'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            
        }
        
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['participants'].queryset = Participant.objects.all() 
        
        self.fields['participants'].widget.attrs.update({'class':'form-control'})
        
class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.EmailInput(attrs={'class':'form-control'}),
            'phone' : forms.TextInput(attrs={'class':'form-control'}),
        }
        
        
        
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description' : forms.Textarea(attrs={'rows' : 3,'class':'form-control'}),
            'icon' : forms.ClearableFileInput(attrs={'class':'form-control'})
        }
        
        
