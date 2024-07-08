from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from .models import Dog
from .ml_model import  load_model,create_data_batches,get_pred_label
import tensorflow as tf
from PIL import Image
import numpy as np
import os
from .models import Contact, Dog
from django.contrib.messages import constants as messages

loaded_full_model = load_model(settings.MODEL_PATH)

def preprocess_image(custom_image_paths):
    custom_data = create_data_batches(custom_image_paths, test_data=True)
    print(custom_data)
    # Make predictions on the custom data
    custom_preds = loaded_full_model.predict(custom_data)
    # Get custom image prediction lbels
    custom_preds_labels = [get_pred_label(custom_preds[i]) for i in range(len(custom_preds))]
    print(custom_preds_labels)

    return custom_preds_labels


def home(request):
    print(settings.MODEL_PATH)

    # print(DEBUG)

    return render(request, 'index.html')




def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST["message"]
        print("post", name, email, subject, message)
        # print(contactName, contactEmail, contactSubject, contactMessage)
        contactFeedback = Contact.objects.create(
            name=name, email=email, subject=subject, message=message)


        try:
            contactSaved = contactFeedback.save()
            print(contactSaved)

            messages.info(
                request, 'Thanks, We get back to you as soon as possible')
            return render(request, "contact.html")
        except:
            messages.warning(request, "Please Try Again, Something Went Wrong")
            return render(request, "contact.html")


    else:
        return render(request, "contact.html")

def uploadDog(request):
    if request.method == 'POST' :
        name = request.POST['name']
        image = request.FILES['image']
        print(name, image)
        print("Entered here")

        # Preprocess the image
        # processed_image = preprocess_image(image)
        # print(f"Processed image shape: {processed_image.shape}")

        # Save the dog entry in the database
        dog_list = []
        dogModel = Dog(name=name, image=image)
        dogModel.save()

         # Get the site domain
        # current_site = get_current_site(request)
        # domain = current_site.domain
        # print("Current site domain: ", domain)

        image_url = dogModel.image.url
        full_image_url = f"{settings.BASE_DIR}{image_url}"


        # print("this is saved here ",dogModel.image.url)
        dog_list.append(full_image_url)
        print(dog_list)
        predicted_label = preprocess_image(dog_list)

        # Make predictions on the peadable label
        # class_names = ['breed1', 'breed2', 'breed3', ...]  # Add your class names here
        # predicted_label = class_names[predicted_class]
        # print(f"Predicted Label: {predicted_label}")rocessed image
        # prediction = loaded_full_model.predict(processed_image)
        # # Get custom image prediction lbels
        # custom_preds_labels = [get_pred_label(custom_preds[i]) for i in range(len(custom_preds))]
        # custom_preds_labels
        # predicted_class = np.argmax(prediction, axis=1)[0]

        # Map predicted_class to a human-r



        context = {
            'name': dogModel.name,
            'pics': dogModel.image,
            'predicted_label': predicted_label[0],
        }
        return render(request, "dog-upload.html", context)
    else:
        return render(request, "dog-upload.html")


