# views.py
from django.shortcuts import render
from django.conf import settings
from django.contrib.messages import constants as messages

from .models import Dog, Contact
from .ml_model import MODEL, create_data_batches, get_pred_label

# -----------------------------
# ML prediction helper
# -----------------------------
def preprocess_image(image_paths):
    data = create_data_batches(image_paths, test_data=True)
    preds = MODEL.predict(data)
    return [get_pred_label(preds[i]) for i in range(len(preds))]

# -----------------------------
# Views
# -----------------------------
def home(request):
    return render(request, "index.html")

def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST["name"],
            email=request.POST["email"],
            subject=request.POST["subject"],
            message=request.POST["message"],
        )
        messages.info(request, "Thanks, we’ll get back to you soon.")
    return render(request, "contact.html")

def uploadDog(request):
    if request.method == "POST":
        dog = Dog.objects.create(
            name=request.POST["name"],
            image=request.FILES["image"]
        )

        image_path = f"{settings.BASE_DIR}{dog.image.url}"
        print("Image path:", image_path)
        predicted_label = preprocess_image([image_path])[0]

        return render(
            request,
            "dog-upload.html",
            {
                "name": dog.name,
                "pics": dog.image.url,
                "predicted_label": predicted_label,
            }
        )

    return render(request, "dog-upload.html")
