from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

# Leaving every field as it is in the AbstractUser model, except for the email field.
class User(AbstractUser):
    # Making the email field unique.
    email = models.EmailField(unique=True)


class UserProfile(models.Model):
    phone= models.CharField(max_length=14, blank=True)
    birth_date=models.DateField(null=True, blank=True)
    profile_pic = models.CharField(max_length=255, blank=True, null=True)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'