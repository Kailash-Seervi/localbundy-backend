from django.db import models
from authentication.models import User

def get_image_path(instance, filename):
    return f"users/{str(instance.author.id)}/{filename}"

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=480, null=True)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    loves = models.ManyToManyField(User, related_name="loves", blank=True)
    views = models.IntegerField(default = 0)
    location = models.CharField(max_length=100, null = True)
    image = models.ImageField("Post image", upload_to=get_image_path, null = True)
    created_at = models.DateTimeField(auto_now_add=True)

