from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# making post model that inherits from models
class Post(models.Model):
    title = models.CharField(max_length=100) # title character field attributes
    content = models.TextField() # unrestricted text
    date_posted = models.DateTimeField(default=timezone.now) # sets the date of the post, though is changeable
    author = models.ForeignKey(User, on_delete=models.CASCADE) # One to many relationship, one user, many posts. If a user is deleted then all posts are deleted

    def __str__(self): # basically how a post is printed out (printed out by title here)
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
