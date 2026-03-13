from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("home/", views.home,name='home'),
    path("signup/",views.register_view,name='signup'),
    path("",views.login_view,name='login'),
    path("Logout/",views.logout_view,name="logout"),
]
