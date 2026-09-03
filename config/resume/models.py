from typing import Iterable

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .utils import user_avatar_path, convert_to_webp
from .validators import phone_validator


class Profile(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    bio = models.TextField()
    avatar = models.ImageField(upload_to=user_avatar_path)
    years_of_experience = models.IntegerField()
    projects_count = models.IntegerField()
    resume_file = models.FileField(upload_to='resume/')
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=20, validators=[phone_validator,])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if self.pk:
            old_avatar = Profile.objects.get(pk=self.pk).avatar

            if self.avatar and old_avatar != self.avatar:
                content = convert_to_webp(self.avatar)
                self.avatar.save('avatar.webp', content, save=False)

                if old_avatar:
                    old_avatar.delete(save=False)

        elif self.avatar:
            content = convert_to_webp(self.avatar)
            self.avatar.save('profile.webp', content, save=False)

        return super().save(*args, **kwargs)


class Experience(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name


class Expertise(models.Model):
    title = models.CharField(max_length=255, unique=True)
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-title']

    def __str__(self):
        return self.title


class Education(models.Model):
    class Degree(models.TextChoices):
        BACHELOR = 'b', "Bachelor's Degree"
        MASTER = 'm', "Master's Degree"
        PHD = 'p', "Doctoral Degree"

    institution = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    degree = models.CharField(max_length=1, choices=Degree.choices)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.institution} - {self.get_degree_display()}'


class SocialLink(models.Model):
    icon = models.ImageField(upload_to='socials_icon/')
    name = models.CharField(max_length=255, unique=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name
