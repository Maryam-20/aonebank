from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import Profiles


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text="Optional")
    last_name = forms.CharField(max_length=30, required=False, help_text="optional")
    email = forms.EmailField(max_length=254, help_text= "Enter a valid email address ")
    
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2"
        ]
    # pass
class User_form(forms.ModelForm):
    
    class Meta:
        model = User
        fields  = [
            "first_name",
            "last_name",
            "email",
        ]
        
class ProfileForm(forms.ModelForm):
    profile_passport = forms.ImageField(required= False, help_text= "Optional")
    particulars = forms.ImageField(required=False, help_text="Optional")
    means_of_identity = forms.ImageField(required=False, help_text="Optional")
    
    
    class Meta:
        model = Profiles
        exclude = [
            "profile",
            "user", 
        ]
        
        widgets =  {
            "date_of_birth": forms.NumberInput(attrs = {"type": "date"}),
            "sex": forms.RadioSelect(),
        }
