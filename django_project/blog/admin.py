from django.contrib import admin
from .models import Post

# Registering models here so they show up on admin page

admin.site.register(Post)