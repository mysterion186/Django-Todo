from django.shortcuts import render
from . import models
from login import models as lg 
# Create your views here.
def liste(request):
    all_list_raw = models.Todos.objects.filter(user = request.user.pk) #affiche les todos de l'utilisateur connecté seulement
    return render(request,"Todos/list.html",{"all_list":all_list_raw,"user":request.user.pk})

def create_todo(request):
    if request.POST:
        user = request.user
        title = request.POST.get("title") 
        infos = request.POST.get("infos")
        print(f"user is {user}\ntitle is {title}\ninfos are {infos} ")
        post = models.Todos(user = user,title = title, infos = infos)
        post.save()
    return render(request,"Todos/create.html")