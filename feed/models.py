from datetime import datetime
from django.contrib.auth.models import User
from django.db import models


# Creating a custom path for storing the user photos
# Example: /MEDIA_ROOT/photos/1234567890/abc.jpg
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

    objects = models.Manager()

    def __str__(self):
        return f"{self.author.username} - {str(self.time)}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
   
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.author.username} - {self.post.id} - {str(self.time)}"
