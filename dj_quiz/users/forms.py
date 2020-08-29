from django import forms
from .models import Participant
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
 
#this form is used to custom create the in-built django form
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'input100','placeholder': 'Enter Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class':'input100','placeholder':'Enter Password'}))


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email


    def __init__(self, *args, **kwargs):
        super(RegisterForm,self).__init__(*args,**kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input100'
            visible.field.widget.attrs['placeholder'] = f'Enter {visible.field.label}'
        self.fields['email'].widget.attrs['placeholder']='Enter Email ID'
 
        

class ParticipantRegForm(forms.ModelForm):
     
     
    class Meta:
        model = Participant
        fields = '__all__'
        widgets = {
            'user':forms.HiddenInput(),
        }
    
    def __init__(self,*args,**kwargs):
        super(ParticipantRegForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input100'
            visible.field.widget.attrs['placeholder'] = f'Enter {visible.field.label}'


        
        self.fields['user'].required = False
        self.fields['phone_no'].required =True

 
        

     
        

    

        
    
    
         
    
 