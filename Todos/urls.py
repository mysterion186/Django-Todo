from django.urls import path
from . import views

app_name = 'todos'
urlpatterns = [
    path("",views.liste,name = "list-todos"),
    path("create/", views.create_todo, name = "create-todos"),
    path("<int:pk>/delete/",views.delete_todo,name = "delete-todos"),
    path("<int:pk>/update/",views.update_todo,name = "update-todos"),
]