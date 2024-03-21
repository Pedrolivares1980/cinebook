from django.db import models
from io import BytesIO
from django.contrib.auth.models import User
from django.core.files.storage import default_storage as storage
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Open the image using the storage backend
        with storage.open(self.image.name, 'rb') as image_file:
            img = Image.open(image_file)

            if img.height > 200 or img.width > 200:
                output_size = (200, 200)
                img.thumbnail(output_size)
                
                # Determine the image format (fallback to JPEG if unknown)
                img_format = img.format if img.format else 'JPEG'
                
                # Save the modified image to a BytesIO/stream
                stream = BytesIO()
                img.save(stream, format=img_format)
                stream.seek(0)
                
                # Save the image back to the storage
                self.image.save(self.image.name, content=stream, save=False)

        super().save(*args, **kwargs)