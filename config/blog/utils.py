import uuid
from PIL import Image
import io
from django.core.files.base import ContentFile



def normalize_title(title):
    title = str(title)
    title = title.strip().replace(' ', '_')

    return title

    
def project_image_path(instance, file_name):
    title = normalize_title(instance.title)
    return f'blog/posts/{title}_{uuid.uuid4()}.webp'


def convert_to_webp(image, quality=100, max_size=(1200, 630)):
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
        name="project.webp"
    )


