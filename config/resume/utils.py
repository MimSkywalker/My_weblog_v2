from pathlib import Path
import uuid
from PIL import Image
import io
from django.core.files.base import ContentFile


def user_avatar_path(instance, file_name):
    file_extension = Path(file_name).suffix
    return f'avatar/{instance.full_name}_{uuid.uuid4()}{file_extension}'


def convert_to_webp(image, quality=80, max_size=(800, 800)):
    with Image.open(image) as img:
        img = img.convert("RGBA")

        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        output = io.BytesIO()
        img.save(
            output,
            format='WEBP',
            method=6,
            quality=quality,
            optimize=True
        )
        output.seek(0)

    return ContentFile(
        output.read(),
        name="profile.webp"
    )