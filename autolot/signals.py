from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, CarPhoto

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, name=instance.username)

@receiver(post_delete, sender=CarPhoto)
def delete_photo_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(False)
