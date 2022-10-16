from uuid import uuid4

from django.db import models
from taggit.managers import TaggableManager

from authy.models import User


class MemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().defer("content")


class Meme(models.Model):
    objects = MemeManager()

    uuid = models.UUIDField(default=uuid4, unique=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.BinaryField()
    content_type = models.CharField(max_length=16)

    tags = TaggableManager()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Meme {self.uuid}"
