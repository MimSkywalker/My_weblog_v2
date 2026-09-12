from django.utils.text import slugify, Truncator
from django.utils.html import strip_tags

from django.db import models
from django.utils import timezone
from django.conf import settings
from .utils import project_image_path, convert_to_webp


class Comment(models.Model):
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='comments', null=False)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    full_name = models.CharField(max_length=120, blank=False)
    email = models.EmailField()
    subject = models.CharField(max_length=256, blank=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.post.title} | {self.subject}'


class Category(models.Model):
    title = models.CharField(max_length=122, unique=True)
    title_en = models.CharField(max_length=122, blank=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *arga, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title_en)
        return super().save(*arga, **kwargs)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'd', 'Draft'
        PUBLISHED = 'p', 'Publisher'
        ARCHIVED = 'a', 'Archives'

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=256)
    title_en = models.CharField(max_length=256)
    feature_image = models.ImageField(upload_to=project_image_path)
    slug = models.SlugField()
    status = models.CharField(
        max_length=1, choices=Status.choices, default=Status.DRAFT)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    categories = models.ManyToManyField(Category, related_name='posts')
    is_featured = models.BooleanField(
        default=False,
        verbose_name="پست ویژه (نمایش بزرگ)",
        help_text="اگر فعال باشد، این پست در بخش «ویژه» بالای صفحهٔ بلاگ به‌صورت بزرگ نمایش داده می‌شود."
    )
    tags = models.ManyToManyField('Tag', related_name='posts')
    meta_description = models.CharField(max_length=161)
    published_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-published_at',)
        indexes = [
            models.Index(fields=['slug', 'status'],
                         name='post_slug_status_idx'),
        ]

    def __str__(self):
        return self.title

    @property
    def word_count(self):
        clean_content = strip_tags(self.content)
        words_count = len(clean_content.split())
        return words_count

    @property
    def reading_time(self):
        reading_time = max(1, self.word_count // 220)
        return reading_time

    def save(self, *args, **kwargs):
        clean_content = strip_tags(self.content)

        if not self.slug:
            self.slug = slugify(self.title_en)

        if self.pk:
            old_image = Post.objects.get(pk=self.pk).feature_image

            if self.feature_image and old_image != self.feature_image:
                content = convert_to_webp(self.feature_image)
                self.feature_image.save('image.webp', content, save=False)

                if old_image:
                    old_image.delete(save=False)

        elif self.feature_image:
            content = convert_to_webp(self.feature_image)
            self.feature_image.save(
                'feature_image.webp', content, save=False)

        now = timezone.now()
        if self.published_at and self.published_at <= now:
            if self.status == self.Status.DRAFT:
                self.status = self.Status.PUBLISHED

        if not self.excerpt:
            self.excerpt = Truncator(clean_content).words(30)
        if not self.meta_description:
            self.meta_description = Truncator(clean_content).chars(160)

        return super().save(*args, **kwargs)


class Tag(models.Model):
    title = models.CharField(max_length=122, unique=True)
    title_en = models.CharField(max_length=122, blank=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def save(self, *arga, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title_en)
        return super().save(*arga, **kwargs)

    def __str__(self):
        return self.title
