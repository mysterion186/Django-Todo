from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
    path('',views.home,name = 'home'),
    path('login/', views.user_login, name = 'login'),
    path('logout/',views.user_logout, name = "logout"),
    path("register/",views.user_register,name = "register"),
    path('activate/<slug:uidb64>/<slug:token>/',views.activate_account,name = 'activate'),
    path("change_password/",views.update_password, name = "change_password"),
    path("changed_password/",views.changed_password, name = "changed_password"),
    path("reset_password/",views.email_reset_password, name = "email_reset_password"),#on met le lien pour recevoir un mail
    path("reset_password/activation/<slug:uidb64>/<slug:token>/",views.reset_password,name = "reset_password"),
    
]