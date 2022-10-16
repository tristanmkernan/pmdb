import os

import magic

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from memedb.models import Meme

User = get_user_model()


class Command(BaseCommand):
    help = "Imports a folder of images for the user with the given tags"

    def add_arguments(self, parser):
        parser.add_argument("user_id", type=int)
        parser.add_argument("tags", type=str)
        parser.add_argument("folder", type=str)

    def handle(self, *args, **options):
        tags = options["tags"].split(",")
        folder = options["folder"]
        user = User.objects.get(pk=options["user_id"])

        for file in os.listdir(folder):
            with open(os.path.join(folder, file), "rb") as handle:
                content = handle.read()
                content_type = magic.from_buffer(content, mime=True)

                meme = Meme.objects.create(
                    owner=user, content=content, content_type=content_type
                )

                meme.tags.add(*tags)

        self.stdout.write(self.style.SUCCESS("Successfully imported folder"))
