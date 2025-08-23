from abc import ABC, abstractmethod
from django.core.files.uploadedfile import UploadedFile
from api.entity.uploaded_image import UploadedImage

class IImageService(ABC):
    @abstractmethod
    def save_image(self, image_file: UploadedFile) -> UploadedImage:
        pass
