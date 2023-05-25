from django.urls import path
from . import views

app_name = "Plant_Data"

urlpatterns = [ 
    path("setDetails/", views.setDetails),
    path("getDetails/", views.getDetails),
    # path("addCartUpdate/", views.addCartUpdate)
]