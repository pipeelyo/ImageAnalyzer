from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.ml.trainer import train_model
import threading

class TrainModelView(APIView):
    def post(self, request):
        train_path = request.data.get('train_path')
        test_path = request.data.get('test_path')

        if not train_path:
            return Response({"error": "train_path is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Run training in a separate thread to avoid blocking the response? 
        # For simplicity in this phase, we might run it synchronously or 
        # just let the user know it started. 
        # Given the user wants to "see" it happen, sync might be better for now 
        # to return the result, although it might timeout.
        # Let's try synchronous first as it's easier to debug errors.
        
        try:
            metrics = train_model(train_path, test_path or train_path)
            return Response({
                "message": "Training completed successfully",
                "metrics": metrics
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
