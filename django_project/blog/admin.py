from django.contrib import admin
from .models import Post
from .models import Post, Category, Tag

#Registering category, tag, and post in the admin site, allowing admins to add such.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)

# Registering models here so they show up on admin page