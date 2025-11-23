from django.shortcuts import render
from django.views import View
from django.core.files.storage import FileSystemStorage
from api.ml.classifier import ClassifierService
import os
from django.conf import settings
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server
import matplotlib.pyplot as plt
import io
import base64

class AnalyzeImageView(View):
    def get(self, request):
        return render(request, 'api/upload.html')

    def post(self, request):
        if 'image' not in request.FILES:
            return render(request, 'api/upload.html', {'error': 'No se ha subido ninguna imagen'})

        image_file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        uploaded_file_url = fs.url(filename)
        file_path = fs.path(filename)

        try:
            # Call ML Service
            service = ClassifierService()
            classification_map, perfil = service.predict(file_path)

            # Generate visualization for the web
            plt.figure(figsize=(8, 8))
            plt.imshow(classification_map, cmap="coolwarm")
            plt.axis("off")
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()
            plt.close()

            result_image_url = f"data:image/png;base64,{image_base64}"

            return render(request, 'api/result.html', {
                'result_image_url': result_image_url,
                'uploaded_file_url': uploaded_file_url
            })

        except Exception as e:
            return render(request, 'api/upload.html', {'error': str(e)})
