from django.urls import path
from dog import views

urlpatterns = [
    path('', views.home,name="home" ),
    path("contact/", views.contact, name="contact"),
    path("dog-upload/", views.uploadDog, name="dog-upload")
]
