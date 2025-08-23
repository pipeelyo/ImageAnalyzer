from django.core.files.uploadedfile import UploadedFile
from api.entity.uploaded_image import UploadedImage
from api.services.i_image_service import IImageService

class ImageServiceImpl(IImageService):
    def save_image(self, image_file: UploadedFile) -> UploadedImage:
        uploaded_image = UploadedImage.objects.create(image=image_file)
        return uploaded_image
