from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from api.services.i_image_service import IImageService
from api.implement.image_service_impl import ImageServiceImpl
from api.model.image_dto import UploadedImageDto

class ImageController(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image_service: IImageService = ImageServiceImpl()

    def post(self, request, *args, **kwargs):
        image_file = request.data.get('image')
        if not image_file:
            return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            saved_image = self.image_service.save_image(image_file)
            serializer = UploadedImageDto(saved_image)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
