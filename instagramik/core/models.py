from django.contrib.auth.models import AbstractUser
from django.db import models


def user_avatar_path(instance, filename):
    user_id = instance.id
    return "user_avatars/user-{}/{}".format(user_id, filename)


class CustomUser(AbstractUser):
    birth_date = models.DateField(blank=True, null=True)
    about = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path)
    friends = models.ManyToManyField('self', blank=True)