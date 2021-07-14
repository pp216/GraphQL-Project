from django.apps import apps
from django.contrib import admin


from .models import User,Post,Tag

admin.site.register(User)
app = apps.get_app_config('graphql_auth')
for model_name, model in app.models.items():
    admin.site.register(model)

admin.site.register(Post)
admin.site.register(Tag)
