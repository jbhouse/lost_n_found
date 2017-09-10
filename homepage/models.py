from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
# Create your models here.

class FoundItemManager(models.Manager):
    def create_found_item(self, user, latitude, longitude, description):
        found_item = self.create(user = user, latitude = latitude, longitude = longitude, description=description)
        return found_item

class LostItemManager(models.Manager):
    def create_lost_item(self, user, latitude, longitude, description):
        lost_item = self.create(user = user, latitude = latitude, longitude = longitude, description=description)
        return lost_item

class FoundItem(models.Model):
    description = models.TextField()
    user = models.ForeignKey(User,related_name='founditems')
    created_at = models.DateTimeField(auto_now=True)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    objects = FoundItemManager()

class LostItem(models.Model):
    description = models.TextField(blank=False)
    user = models.ForeignKey(User,related_name='lostitems')
    created_at = models.DateTimeField(auto_now=True)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    objects = LostItemManager()

# our user profile, (one to one linked model that corresponds with a specific user)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=14,blank=True)
    emailable = models.BooleanField(default=False)
    textable = models.BooleanField(default=False)

# this code "attaches" these methods to the user model, and calls them whenever a save event occurs
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
