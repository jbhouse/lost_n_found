from django.db import models
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth import models
from django.contrib.auth.models import User

class User(auth.models.User, auth.models.PermissionsMixin):

    class Meta:
        auto_created = True        

    def __str__(self):
        return "@{}".format(self.get_username())
