from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm, remove_perm
from ..models import Meme


@receiver(post_save, sender=Meme)
def set_permissions(sender, instance: Meme, **kwargs):
    """
    thanks to https://dandavies99.github.io/posts/2021/11/django-permissions/
    """
    # Get permission codenames
    view = f"view_{instance._meta.model_name}"
    change = f"change_{instance._meta.model_name}"
    delete = f"delete_{instance._meta.model_name}"

    # Assign the creator all permissions
    assign_perm(view, instance.owner, instance)
    assign_perm(change, instance.owner, instance)
    assign_perm(delete, instance.owner, instance)
