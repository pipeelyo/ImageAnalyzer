from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from api.ml.trainer import train_model
import threading
import os

class TrainModelView(APIView):
    def post(self, request):
        # Use default paths from settings if not provided
        train_path = request.data.get('train_path', settings.ML_TRAIN_PATH)
        test_path = request.data.get('test_path', settings.ML_TEST_PATH)

        # Validate paths exist
        if not os.path.exists(train_path):
            return Response({
                "error": f"Train path does not exist: {train_path}"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not os.path.exists(test_path):
            return Response({
                "error": f"Test path does not exist: {test_path}"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            metrics = train_model(train_path, test_path)
            return Response({
                "message": "Training completed successfully",
                "train_path": train_path,
                "test_path": test_path,
                "metrics": metrics
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": str(e),
                "train_path": train_path,
                "test_path": test_path
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
