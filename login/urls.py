from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
    path('',views.home,name = 'home'),
    path('login/', views.user_login, name = 'login'),
    path('logout/',views.user_logout, name = "logout"),
    path("register/",views.user_register,name = "register"),
    path('activate/<slug:uidb64>/<slug:token>/',views.activate_account,name = 'activate')
    
]