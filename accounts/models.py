# from django.db import models
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth import models
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class User(auth.models.User, auth.models.PermissionsMixin):

    class Meta:
        auto_created = True

    def __str__(self):
        return "@{}".format(self.get_username())

# # our user profile, (one to one linked model that corresponds with a specific user)
# class Profile(models.Model):
#     user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
#     phone_number = models.TextField(max_length=500, blank=True)
#     emailable = models.BooleanField()
#     textable = models.BooleanField()
#
# # this code "attaches" these methods to the user model, and calls them whenever a save event occurs
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
