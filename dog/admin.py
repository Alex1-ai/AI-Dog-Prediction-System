from django.contrib import admin

# Register your models here.
from . import models
# Register your models here.

admin.site.site_header = 'Dog Prediction Admin'
admin.site.index_title = 'Admin'



@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email',
                    'subject', 'message' ]



@admin.register(models.Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ['name', "image" ]