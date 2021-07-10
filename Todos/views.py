from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from . import models
from login import models as lg 
from Todo import settings

from django.core.mail import EmailMessage, EmailMultiAlternatives

# Create your views here.
#  display all user's todo
def liste(request):
    all_list_raw = models.Todos.objects.filter(user = request.user.pk) 
    return render(request,"Todos/list.html",{"all_list":all_list_raw,"user":request.user.pk})

# allow a user to create a new todo  
def create_todo(request):
    if request.POST:
        user = request.user
        title = request.POST.get("title") 
        infos = request.POST.get("infos")
        print(f"user is {user}\ntitle is {title}\ninfos are {infos} ")
        post = models.Todos(user = user,title = title, infos = infos)
        post.save()
    return render(request,"Todos/create.html")

#allow the user to delete a todo
def delete_todo(request,pk):
    post = models.Todos.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse('todos:list-todos'))

def update_todo(request,pk):
    post = models.Todos.objects.get(pk=pk)
    # if the user send a post request after modifing the todo
    if request.POST : 
        title = request.POST.get("Title")
        infos = request.POST.get('info')
        post.title = title
        post.infos = infos
        post.save()
        return HttpResponseRedirect(reverse("todos:list-todos"))
    # display the "form" for updating the todo
    else : 
        return render(request,'Todos/update.html',{"post":post}) 

#test pour envoyer des emails généralisé
def send_all_email(request):
    queryset = lg.MyUser.objects.all() #on prend tous les emails présent dans la base de données 
    to = []
    for mail in queryset : 
        to.append(mail)
    # on s'attend à recevoir un post request pour envoyer les emails à tous le monde 
    if request.POST :
        # on choppe le sujet et le texte de l'email à envoyer
        subject = request.POST.get("subject")
        email = request.POST.get("email")  
        from_email = settings.EMAIL_HOST_USER
        msg = EmailMultiAlternatives(subject, '', from_email, to)
        msg.attach_alternative(email, "text/html")
        msg.send()
        return HttpResponse("On a envoyé l'email à tous les membres de la base de données ")
    return render(request,"general_email.html")