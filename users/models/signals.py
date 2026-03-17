from django.db.models.signals import post_delete
from django.dispatch import receiver

from users.models import User


@receiver(post_delete, sender=User)
def delete_avatar_on_user_delete(sender, instance: User, **kwargs):
    if instance.avatar:
        instance.avatar.delete(save=False)  # type: ignore[reportAttributeAccessIssue]
