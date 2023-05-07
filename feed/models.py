from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.contrib.auth.models import User


# Create your models here.


# Creating a custom path for storing the user photos
# Example : /MEDIA_ROOT/photos/1234567890/abc.jpg
def path(instance, filename):
    return 'photos/{0}/{1}'.format(instance.author.username, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    display = models.FileField(blank=True, null=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_written')
    caption = models.TextField(max_length=500)
    photo = models.FileField(upload_to=path)
    likes = models.ManyToManyField(User, related_name='posts_liked', blank=True)
    time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.author.username + " - " + str(self.time)


'''
    def save(self, *args, **kwargs):
    if not self.id:
        self.time = timezone.now()
    return super(Post, self).save(*args, **kwargs)
'''


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.author.username + " - " + self.post.id + " - " + self.time
