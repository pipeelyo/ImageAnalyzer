from rest_framework import serializers
from api.entity.uploaded_image import UploadedImage

class UploadedImageDto(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ('id', 'image', 'uploaded_at')
