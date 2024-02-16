from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    year_of_birth = models.IntegerField()
    country = models.CharField(max_length=50)
    def __str__(self):
        return self.first_name+" "+self.last_name

class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Blogger, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="images/")
    created =models.DateTimeField()
    modified = models.DateTimeField()
    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(null=True, blank=True)
    created = models.DateTimeField()
    author = models.ForeignKey(Blogger, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)

class BlockedUser(models.Model):
    user = models.ForeignKey(Blogger, on_delete=models.CASCADE, related_name='blocked_users')
    blocked_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by')
