from django.core.management.base import BaseCommand
from api.ml.trainer import train_model
import os

class Command(BaseCommand):
    help = 'Train the ML model from CLI'

    def add_arguments(self, parser):
        parser.add_argument('--train_path', type=str, required=True, help='Path to training images')
        parser.add_argument('--test_path', type=str, required=False, help='Path to test images')

    def handle(self, *args, **options):
        train_path = options['train_path']
        test_path = options['test_path'] or train_path

        if not os.path.exists(train_path):
            self.stdout.write(self.style.ERROR(f'Train path not found: {train_path}'))
            return

        self.stdout.write(f'Starting training with images from: {train_path}')
        try:
            metrics = train_model(train_path, test_path)
            self.stdout.write(self.style.SUCCESS(f'Training completed successfully! Metrics: {metrics}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Training failed: {str(e)}'))
