from django.urls import path
from api.controller.image_controller import ImageController
from api.views_ml import TrainModelView
from api.views_ui import AnalyzeImageView
from api.views_api import AnalyzeImageAPIView

urlpatterns = [
    path('upload/', ImageController.as_view(), name='image-upload'),
    path('train/', TrainModelView.as_view(), name='train_model'),
    path('analyze/', AnalyzeImageView.as_view(), name='analyze_image'),  # HTML view (legacy)
    path('analyze-api/', AnalyzeImageAPIView.as_view(), name='analyze_image_api'),  # JSON API
]
