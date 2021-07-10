from django.shortcuts import render 
from django.contrib import messages

#pour envoyer des mails : 
from django.contrib.sites.shortcuts import get_current_site 
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template # charger une page html
from Todo import settings
#permet de gérer tout ce qui est en rapport avec la connexion/déconnexion de l'utilisateur
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
#affichage de page selon la situation 
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse 

from django.template.loader import render_to_string #convertit une page html en mail pour envoyer le lien d'activation 
#création d'outil pour créer/décoder des ine time link
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token

#formulaire pour que les gens puissent s'enregistrer
from .forms import CustomUserCreationForm, CustomUserChangePassword

#import du modèle d'utilisateur que l'on a créé
from .models import MyUser


from django.contrib.auth.decorators import login_required


#home page
def home(request):
    return render(request,'home.html')
#login page
def user_login(request):
    if request.POST :
        email = request.POST.get("email") 
        password = request.POST.get("password")
        user = authenticate(email = email, password = password)
        #check if the user exists and if it's account is active
        if user is not None and user.is_active :
            login(request,user)
            return HttpResponseRedirect(reverse('login:home'))
        return render(request,'login/login.html')
    return render(request,'login/login.html')

#logout page
def user_logout(request):
    logout(request) 
    return HttpResponseRedirect(reverse('login:home'))

#register page
def user_register(request):
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        #partie pour l'envoie d'un email d'activation 
        # current_site = get_current_site(request)
        # email_subject = 'Activation de votre compte'
        # message = render_to_string('login/activate_account.html',
        #         {'user':user,'domain':current_site,
        #         'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        #         'token': account_activation_token.make_token(user),})

        # to_email = form.cleaned_data.get('email')
        # email = EmailMessage(email_subject,message,to =[to_email])
        # email.send()
        subject, from_email, to = 'Activation de votre compte', settings.EMAIL_HOST_USER, form.cleaned_data.get('email')
        text_content = ''
        # = render_to_string("login/activate_account.html")#'<p>This is an <strong>important</strong> message.</p>'
        html_content = f"Hi {user.username}\nPlease click on the link to confirm your registration http://{get_current_site(request)}/{account_activation_token.make_token(user)}\n<p  style='color: blue;' >Test couleur bleue</p>"
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return HttpResponse("On vous a envoyé un email, cliquez sur le lien pour terminer votre inscription ")
    else :
        form = CustomUserCreationForm()
    return render(request,'login/register.html',{'form':form})

#activate account
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
    
#change password
@login_required
def update_password(request):
    if request.method =='POST':
        form = CustomUserChangePassword(request.user,request.POST)
        if form.is_valid() :
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request,'Your password was successfully updated !')
            return HttpResponseRedirect(reverse('login:changed_password'))
        else :
            messages.error(request,'Please correct the error below.')
    else :
        form = CustomUserChangePassword(request.user)
    return render(request,'login/change_password.html',{'form':form})

#temp page to say that the password has been changed
def changed_password(request):
    return render(request,'login/changed.html')

#reset a forgotten password
def email_reset_password(request):
    if request.POST:
        email = request.POST.get("email")
        #on vérifie qu'un compte avec cette adresse mail existe
        try :
            user = MyUser.objects.get(email=email)
        except:
            return HttpResponse("Compte n'existe pas") 
        current_site = get_current_site(request)
        email_subject = 'Réinitilisation de votre mot de passe '
        message = render_to_string('login/reset_password_real.html',
                {'user':user,'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),})
        to_email = email
        email = EmailMessage(email_subject,message,to =[to_email])
        email.send()
        return HttpResponse("On vous a envoyé un email, cliquez sur le lien pour terminer votre inscription ")
    return render(request,"login/reset_password.html")

#activate account
def reset_password(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.POST:
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            if password1 == password2:
                user.set_password(password2)
                user.save()
            return HttpResponse('Your account has been activate successfully')
        else :
            return render(request,'login/reset_slug_password.html')
    else:
        return HttpResponse('Activation link is invalid!')