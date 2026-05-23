from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("signup/", views.register_view, name="signup"),
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("health/", views.health_check, name="health_check"),
]
