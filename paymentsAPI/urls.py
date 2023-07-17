from django.urls import path

from . import views

urlpatterns = [
    path('order/', views.createNewOrder, name="createNewOrder"),
    path('verify/', views.verifyPayment, name="verifyPayment")
]
