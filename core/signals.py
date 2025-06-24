from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import User, UserProfile

# Signal to create a new UserProfile when a new User is registered
@receiver(post_save, sender=User)
def create_user_profile_for_new_user(sender, **kwargs):
    print("It's working")
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])