from uuid import uuid4

from django.db import models
from taggit.managers import TaggableManager

from authy.models import User
from memedb.utils import is_image_content_type


class MemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().defer("content")


class Meme(models.Model):
    objects = MemeManager()

    uuid = models.UUIDField(default=uuid4, unique=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.BinaryField()
    content_type = models.CharField(max_length=16)
    comparison_hash = models.CharField(max_length=2048, blank=True, null=True)

    tags = TaggableManager()

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_image(self):
        return is_image_content_type(self.content_type)

    def __str__(self) -> str:
        return f"Meme {self.uuid}"
