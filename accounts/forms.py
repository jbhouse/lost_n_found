from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from homepage.models import Profile
from django.contrib.auth.models import User

class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ('username','email','password1','password2')
        model = get_user_model()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = 'Display Name'
        self.fields['email'].label = 'Email Address'

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number', 'emailable', 'textable')
