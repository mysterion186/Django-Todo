from django.shortcuts import render
from django.http import HttpResponseRedirect 
from django.urls import reverse

from . import models
from login import models as lg 
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
    