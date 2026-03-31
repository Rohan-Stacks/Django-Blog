from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

# Category model used to group posts into predefined sections
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True) # Name of the category (e.g. School)
    slug = models.SlugField(unique=True, blank=True) # (slugs ensuring that special characters in categories or tags do not break the website's URL structure) URL-friendly version of the name

    def save(self, *args, **kwargs):
        # Automatically generate slug from name if not already set
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Tag model used for flexible labels that users can add themselves
class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True) # Tag name entered by user
    slug = models.SlugField(unique=True, blank=True) # Clean URL version

    def save(self, *args, **kwargs):
        # Automatic slug generation for consistency and filtering
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# making post model that inherits from models
class Post(models.Model):
    title = models.CharField(max_length=100) # title character field attributes
    content = models.TextField() # unrestricted text
    date_posted = models.DateTimeField(default=timezone.now) # sets the date of the post, though is changeable
    author = models.ForeignKey(User, on_delete=models.CASCADE) # One-to-many relationship, one user, many posts. If a user is deleted then all posts are deleted
    is_private = models.BooleanField(default=False)  # private post flag

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='posts'
    )

    def __str__(self): # basically how a post is printed out (printed out by title here)
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
