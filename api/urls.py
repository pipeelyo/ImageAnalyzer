from django.urls import path
from api.controller.image_controller import ImageController

urlpatterns = [
    path('upload/', ImageController.as_view(), name='image-upload'),
]
