from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Snippet
from .tasks import send_email_in_snippet_creation

@receiver(post_save, sender=Snippet)
def snippet_created_handler(sender, instance, created, **kwargs):
    """
    Signal handler that sends an email when a Snippet instance is created.
    """
    if created:
        user_mail = instance.user.email if instance.user else None
        send_email_in_snippet_creation.delay(instance.name, instance.description, user_mail)
