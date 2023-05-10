from django.urls import path

from . import views

app_name = "AuthAPI"
urlpatterns = [
    path("login/", views.authAPILogin),
    path("signup/", views.authAPISignUp)
]