from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import ManyToManyField


class User(AbstractUser):
    email=models.EmailField(blank=False, max_length=255, verbose_name="email")
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

class Tag(models.Model):
    name=models.CharField(max_length=255)


    def __str__(self):
        return self.name

class Post(models.Model):
    user=models.ForeignKey(User,default=1,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=200)
    tags = ManyToManyField(Tag)

    def __str__(self):
        return self.title