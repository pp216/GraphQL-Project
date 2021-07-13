from django.db import models
from django.db.models import ManyToManyField
from django.utils.translation import gettext_lazy as _

class UserRegistration(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    def __str__(self):
        return self.username

class Tag(models.Model):
    name=models.CharField(max_length=255)


    def __str__(self):
        return self.name

class post(models.Model):
    user=models.ForeignKey(UserRegistration,default=1,on_delete=models.DO_NOTHING)
    title=models.CharField(max_length=255)
    description=models.CharField(max_length=200)
    tags=ManyToManyField(Tag)
    def __str__(self):
        return self.title




