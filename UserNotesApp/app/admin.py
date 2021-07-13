from django.contrib import admin
from . import models
from .models import Tag


@admin.register(models.UserRegistration)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'email',
    ]
@admin.register(models.post)
class PostAdmin(admin.ModelAdmin):
    list_display = [

        'title',
        'description',
    ]
admin.site.register(Tag)
