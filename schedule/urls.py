from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("edit", views.edit, name="edit")
]
