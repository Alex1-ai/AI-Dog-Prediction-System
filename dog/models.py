from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=254)
    message = models.TextField()



class Dog(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='dogs/')
