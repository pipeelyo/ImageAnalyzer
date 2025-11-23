from django.core.management.base import BaseCommand
from api.ml.classifier import ClassifierService
import os
import numpy as np

class Command(BaseCommand):
    help = 'Test the ML model on a specific image'

    def add_arguments(self, parser):
        parser.add_argument('--image', type=str, required=True, help='Path to the image to classify')
        parser.add_argument('--output', type=str, required=False, help='Path to save the output classification')

    def handle(self, *args, **options):
        image_path = options['image']
        output_path = options['output']

        if not os.path.exists(image_path):
            self.stdout.write(self.style.ERROR(f'Image not found: {image_path}'))
            return

        self.stdout.write(f'Classifying image: {image_path}...')
        
        service = ClassifierService()
        try:
            classification_map, perfil = service.predict(image_path)
            
            unique, counts = np.unique(classification_map, return_counts=True)
            stats = dict(zip(unique, counts))
            self.stdout.write(self.style.SUCCESS(f'Classification successful! Stats: {stats}'))

            if output_path:
                service.save_classification(classification_map, perfil, output_path)
                self.stdout.write(self.style.SUCCESS(f'Saved classification to: {output_path}'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during classification: {str(e)}'))
