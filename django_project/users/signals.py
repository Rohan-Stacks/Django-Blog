from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, ** kwargs) :
    if created:
        Profile.objects.create(user=instance)

@receiver (post_save, sender=User)
def save_profile(sender, instance, ** kwargs) :
    instance.profile.save()

# These signals automatically create a Profile whenever a new User is made,
# and make sure the Profile is saved whenever the User is saved.