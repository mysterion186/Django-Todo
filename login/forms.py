
from .models import MyUser
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm 

class CustomUserCreationForm(UserCreationForm):
    #think I neek to add extrafields here and the main parts go into the Meta
    password1 = forms.CharField(widget = forms.PasswordInput())
    password2 = forms.CharField(widget = forms.PasswordInput())
    class Meta(UserCreationForm):
        model = MyUser
        fields = ('email','username','password1','password2')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = MyUser
        fields = ('email',)
    
class CustomUserChangePassword(PasswordChangeForm):
    old_password = forms.CharField(widget = forms.PasswordInput())
    new_password1 = forms.CharField(widget = forms.PasswordInput())
    new_password2 = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = MyUser
        fields = ('old_password','new_password1','new_password2') 
    
