from django.utils.text import slugify
from django.db import models
from .utils import convert_to_webp, project_image_path


class Project(models.Model):
    title = models.CharField(max_length=256, unique=True)
    image = models.ImageField(
        upload_to=project_image_path, blank=True, null=True)
    description = models.TextField()
    employer = models.CharField(max_length=256)
    date_of_implementation = models.DateField()
    technologies = models.ManyToManyField(
        'Technology', related_name='projects')
    categories = models.ManyToManyField('Category', related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        if self.pk:
            old_image = Project.objects.get(pk=self.pk).image

            if self.image and old_image != self.image:
                content = convert_to_webp(self.image)
                self.image.save('image.webp', content, save=False)

                if old_image:
                    old_image.delete(save=False)

        elif self.image:
            content = convert_to_webp(self.image)
            self.image.save('image.webp', content, save=False)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_of_implementation']


class Technology(models.Model):
    title = models.CharField(max_length=256, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)
