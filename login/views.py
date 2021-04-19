from django.shortcuts import render 
from django.contrib.sites.shortcuts import get_current_site 
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse 
from django.core.mail import EmailMessage
from .forms import CustomUserCreationForm
from .models import MyUser
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
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
        current_site = get_current_site(request)
        email_subject = 'Activation de votre compte'
        message = render_to_string('activate_account.html',{'user':user,'domain':current_site,'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),})
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(email_subject,message,to =[to_email])
        email.send()
        # return HttpResponseRedirect(reverse('login:home'))
        return HttpResponse("On vous a envoyé un email, cliquez sur le lien pour terminer votre inscription ")
    else :
        form = CustomUserCreationForm()
    return render(request,'login/register.html',{'form':form})

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activate successfully')
    else:
        return HttpResponse('Activation link is invalid!')