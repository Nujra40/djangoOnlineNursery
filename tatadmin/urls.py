from django.urls import path

from . import views

app_name = "admin"
urlpatterns = [
    path('getAllOrders/', views.getAllOrders, name="getAllOrders"),
    path('getPendingOrders/', views.getPendingOrders, name="getPendingOrders"),
    path('updateStatus/', views.updateStatus, name="updateStatus")
]