from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
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
