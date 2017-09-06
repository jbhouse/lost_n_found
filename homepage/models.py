from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class FoundItemManager(models.Manager):
    def create_found_item(self, user):
        found_item = self.create(user = user)
        return found_item

class LostItemManager(models.Manager):
    def create_lost_item(self, user):
        lost_item = self.create(user = user)
        return lost_item

class FoundItem(models.Model):
    description = models.TextField(blank=False)
    user = models.ForeignKey(User,related_name='founditems')
    created_at = models.DateTimeField(auto_now=True)
    latitude = models.IntegerField(blank=False)
    longitude = models.IntegerField(blank=False)
    objects = FoundItemManager()

class LostItem(models.Model):
    description = models.TextField(blank=False)
    user = models.ForeignKey(User,related_name='lostitems')
    created_at = models.DateTimeField(auto_now=True)
    latitude = models.IntegerField(blank=False)
    longitude = models.IntegerField(blank=False)
    objects = LostItemManager()
