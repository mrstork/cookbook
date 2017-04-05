import math
from io import BytesIO
from PIL import Image
from django.core.exceptions import ValidationError
from django.forms import ImageField as DjangoImageField

# Most of this code is taken from the django source for ImageField
# modifications made ensure uploaded image is a 800 x 450 PNG under 1 MB

class PNGField(DjangoImageField):
    default_error_messages = {
        'invalid_image': (
            'Upload a valid png. The file you uploaded was either not a png or is corrupt.'
        ),
        'invalid_image_file_size': (
            'Upload a smaller png. The file you uploaded was larger than 1 MB.'
        ),
        'invalid_image_resolution': (
            'Uploaded png must be 800 x 450.'
        ),
    }
    def to_python(self, data):
        """
        Check that the uploaded file is a valid png
        """
        f = super().to_python(data)
        if f is None:
            return None

        from PIL import Image

        if hasattr(data, 'temporary_file_path'):
            file = data.temporary_file_path()
        else:
            if hasattr(data, 'read'):
                file = BytesIO(data.read())
            else:
                file = BytesIO(data['content'])

        try:
            image = Image.open(file)
            image.verify()

            f.image = image
            content_type = Image.MIME.get(image.format)
            f.content_type = content_type

            # Force image to be a png
            if content_type != 'image/png':
                raise ValidationError(
                    self.error_messages['invalid_image'],
                    code='invalid_image',
                )

            # Ensure file size is below limit
            if f.size > math.pow(10, 6):
                raise ValidationError(
                    self.error_messages['invalid_image_file_size'],
                    code='invalid_image_file_size',
                )

            # Validate image resolution
            if image.width != 800 or image.height != 449:
                raise ValidationError(
                    self.error_messages['invalid_image_resolution'],
                    code='invalid_image_resolution',
                )

        except Exception as exc:
            # Pillow doesn't recognize uploaded file as an image.
            raise ValidationError(
                self.error_messages['invalid_image'],
                code='invalid_image',
            ) from exc

        if hasattr(f, 'seek') and callable(f.seek):
            f.seek(0)

        return f
