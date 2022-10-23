import math
import io

import imagehash

from django.contrib.auth import get_user_model
from guardian.shortcuts import get_objects_for_user
from PIL import Image

from memedb.models import Meme
from memedb.utils import is_image_content_type

User = get_user_model()


def find_suggested_tags(
    user: User, content: bytes, content_type: str, num_tags=3
) -> list[str]:
    if is_image_content_type(content_type):
        return find_suggested_tags_for_image(user, content, num_tags)

    return []


def find_suggested_tags_for_image(
    user: User, image_data: bytes, num_tags=3
) -> list[str]:
    def compare(other: Meme):
        if other.is_image and other.comparison_hash:
            other_phash = imagehash.hex_to_hash(other.comparison_hash)

            return image_phash - other_phash

        return math.inf

    # convert image data to phash
    image = Image.open(io.BytesIO(image_data))

    image_phash = imagehash.phash(image, hash_size=64)

    # rank comparison to other memes for user
    memes = get_objects_for_user(user, "memedb.view_meme")

    memes_ranked = sorted(
        memes,
        key=compare,
    )

    # return best matching tags
    tags = set()

    for meme in memes_ranked:
        if len(tags) >= num_tags:
            break

        tags |= set(meme.tags.names())

    return list(tags)[:num_tags]


def cache_content_comparison_hash(meme: Meme) -> None:
    if meme.is_image:
        image = Image.open(io.BytesIO(meme.content))

        image_phash = imagehash.phash(image, hash_size=64)

        meme.comparison_hash = str(image_phash)

    # TODO other types of comparison hashing
    # e.g. for webms/gifs
