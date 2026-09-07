from django.db import models


class Contact(models.Model):

    class Status(models.TextChoices):
        UNREVIEWED = 'U', 'Unreviewed'
        REVIEWED = 'R', 'Reviewed'
        AWAITING = 'A', 'Awaiting'

    full_name = models.CharField(max_length=100)
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.UNREVIEWED)
    email = models.EmailField(blank=False)
    subject = models.CharField(max_length=256)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.full_name} - {self.subject}'
