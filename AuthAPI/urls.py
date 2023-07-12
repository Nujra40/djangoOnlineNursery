from django.urls import path

from . import views

app_name = "AuthAPI"
urlpatterns = [
    path("login/", views.authAPILogin),
    path("signup/", views.authAPISignUp),
    path("update/", views.authAPIAddAlt),
    path("csrf/", views.authAPIgetCSRF),
    path("reset/", views.authAPIforgotPassword),
    path("OAuth2/", views.authAPIOAuth2),
    path("cartFunction/", views.cartFunction),
    path("userFunction/", views.userFunction)
]