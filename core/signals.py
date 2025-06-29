from rest_framework.authtoken.models import Token

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from core.models import User, UserProfile

# Signal to create a new UserProfile when a new User is registered
@receiver(post_save, sender=User)
def create_user_profile_for_new_user(sender, **kwargs):
    if kwargs['created']:
        instance = kwargs['instance']
        UserProfile.objects.create(user=instance)
        token = Token.objects.create(user=instance)
        
        # Getting the new user's email
        user_email = instance.email
        
        # Sending an email (console) with an activation link
        link = f'http://localhost:8000/user/activate?email={user_email}&token={token}'
        
        send_mail(
            "Account Activation",
            f"Follow this link to activate your account: {link}",
            "admin@admin.com",
            [user_email],True
        )