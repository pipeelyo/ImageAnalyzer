from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import FileSystemStorage
from api.ml.classifier import ClassifierService
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server
import matplotlib.pyplot as plt
import io
import base64
from PIL import Image
import rasterio
import numpy as np

class AnalyzeImageAPIView(APIView):
    """
    API endpoint para analizar imágenes.
    Devuelve JSON con la imagen de resultado en base64.
    """
    def post(self, request):
        if 'image' not in request.FILES:
            return Response(
                {"error": "No se ha subido ninguna imagen"},
                status=status.HTTP_400_BAD_REQUEST
            )

        image_file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        file_path = fs.path(filename)

        try:
            # Convert TIF to PNG for display
            original_image_url = None
            try:
                with rasterio.open(file_path) as src:
                    # Read RGB bands (bands 1, 2, 3) or first 3 bands
                    bands_to_read = []
                    if src.count >= 3:
                        bands_to_read = [1, 2, 3]  # RGB
                    else:
                        bands_to_read = [1] * 3  # Use first band for all channels
                    
                    # Read bands
                    rgb_data = []
                    for band_idx in bands_to_read:
                        if band_idx <= src.count:
                            band = src.read(band_idx)
                            # Handle multi-dimensional arrays (remove extra dimensions)
                            if len(band.shape) > 2:
                                band = band[0]
                            rgb_data.append(band)
                        else:
                            # If band doesn't exist, use zeros
                            rgb_data.append(np.zeros((src.height, src.width), dtype=src.dtypes[0]))
                    
                    # Stack bands into RGB array
                    if len(rgb_data) == 3:
                        rgb_array = np.dstack(rgb_data)
                    else:
                        rgb_array = rgb_data[0]
                        # Convert grayscale to RGB
                        if len(rgb_array.shape) == 2:
                            rgb_array = np.dstack([rgb_array, rgb_array, rgb_array])
                    
                    # Normalize to 0-255 range
                    if rgb_array.dtype != np.uint8:
                        rgb_array = rgb_array.astype(np.float32)
                        # Handle NaN and Inf values
                        rgb_array = np.nan_to_num(rgb_array, nan=0.0, posinf=0.0, neginf=0.0)
                        
                        # Normalize each channel separately
                        for i in range(3):
                            band = rgb_array[:, :, i]
                            band_min = np.min(band)
                            band_max = np.max(band)
                            if band_max > band_min:
                                rgb_array[:, :, i] = ((band - band_min) / (band_max - band_min) * 255).astype(np.uint8)
                            else:
                                rgb_array[:, :, i] = np.zeros_like(band, dtype=np.uint8)
                        rgb_array = rgb_array.astype(np.uint8)
                    
                    # Ensure values are in valid range
                    rgb_array = np.clip(rgb_array, 0, 255).astype(np.uint8)
                    
                    # Convert to PIL Image
                    pil_image = Image.fromarray(rgb_array, mode='RGB')
                    
                    # Resize if too large (max 2048px on longest side for performance)
                    max_size = 2048
                    if max(pil_image.size) > max_size:
                        ratio = max_size / max(pil_image.size)
                        new_size = (int(pil_image.size[0] * ratio), int(pil_image.size[1] * ratio))
                        pil_image = pil_image.resize(new_size, Image.Resampling.LANCZOS)
                    
                    # Convert to PNG base64
                    img_buf = io.BytesIO()
                    pil_image.save(img_buf, format='PNG')
                    img_buf.seek(0)
                    original_image_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')
                    img_buf.close()
                    original_image_url = f"data:image/png;base64,{original_image_base64}"
            except Exception as e:
                # If conversion fails, continue without original image
                print(f"Warning: Could not convert TIF to PNG: {str(e)}")
                original_image_url = None

            # Call ML Service
            service = ClassifierService()
            classification_map, perfil = service.predict(file_path)

            # Generate visualization
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

            return Response({
                "result_image_url": result_image_url,
                "original_image_url": original_image_url,
                "uploaded_file_url": fs.url(filename),
                "message": "Imagen clasificada exitosamente"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

