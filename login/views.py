from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm
# Create your views here.

def home(request):
    return render(request,'home.html')

def user_login(request):
    if request.POST :
        print(request)
        email = request.POST.get("email") 
        password = request.POST.get("password")
        user = authenticate(email = email, password = password)
        #check if the user exists and if it's account is active
        if user is not None and user.is_active :
            login(request,user)
            return HttpResponseRedirect(reverse('login:home'))
        return render(request,'login/login.html')
    return render(request,'login/login.html')

def user_logout(request):
    logout(request) 
    return HttpResponseRedirect(reverse('login:home'))

def user_register(request):
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()

        return HttpResponseRedirect(reverse('login:home'))
    else :
        form = CustomUserCreationForm()
    return render(request,'login/register.html',{'form':form})