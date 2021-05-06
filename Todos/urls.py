from django.urls import path
from . import views

app_name = 'todos'
urlpatterns = [
    path("",views.liste,name = "list-todos"),
    path("create/", views.create_todo, name = "create-todos")
]