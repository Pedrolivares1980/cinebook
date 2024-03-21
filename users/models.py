from django.db import models
from django.contrib.auth.models import User
from PIL import Image, UnidentifiedImageError
from django.core.files.storage import default_storage as storage
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics/')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # Check if the current instance has an existing profile
        if self.pk:
            old_profile = Profile.objects.get(pk=self.pk)
            # If the old profile has a different image than the current one, delete the old image
            if old_profile.image.name != 'default.jpg' and old_profile.image.name != self.image.name:
                storage.delete(old_profile.image.name)

        # Process the new image
        if self.image:
            try:
                with storage.open(self.image.name, 'rb') as img_read:
                    img = Image.open(img_read)
                    original_format = img.format
                    
                    # Check and adjust image orientation based on EXIF data
                    if hasattr(img, '_getexif'):
                        exif = img._getexif()
                        orientation = exif.get(0x0112) if exif else None
                        if orientation == 3:
                            img = img.rotate(180, expand=True)
                        elif orientation == 6:
                            img = img.rotate(270, expand=True)
                        elif orientation == 8:
                            img = img.rotate(90, expand=True)

                    # Resize the image if it is larger than the maximum allowed size
                    if img.height > 300 or img.width > 300:
                        output_size = (300, 300)
                        img.thumbnail(output_size)

                        # Save the processed image to a BytesIO object
                        in_mem_file = BytesIO()
                        img.save(in_mem_file, format=original_format)
                        in_mem_file.seek(0)

                        # Write the processed image back to storage
                        with storage.open(self.image.name, 'wb+') as img_write:
                            img_write.write(in_mem_file.getvalue())
            except UnidentifiedImageError:
                # Log an error if the file is not a valid image
                logger.error(f'Error processing image for user {self.user.username}: File is not a valid image.')
            except Exception as e:
                # Log any unexpected errors
                logger.error(f'Unexpected error processing image for user {self.user.username}: {e}')

        # Call the superclass method to save the object
        super().save(*args, **kwargs)
