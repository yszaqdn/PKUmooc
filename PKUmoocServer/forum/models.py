from django.db import models
from django.utils import timezone
from user_info.models import User
# from django.contrib.auth.models import User

# Create your models here.
class Forum(models.Model):
    name = models.CharField(max_length=100, verbose_name="讨论区")
    def __str__(self):
        return self.name

class ForumSection(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, verbose_name="讨论区")
    name = models.CharField(max_length=100,verbose_name="板块")
    def __str__(self):
        return self.name

class Post(models.Model):
    section = models.ForeignKey(ForumSection, on_delete=models.CASCADE, verbose_name="板块")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="帖子")
    created_at = models.DateTimeField(default=timezone.now,verbose_name="发布时间")
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return self.content

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="帖子")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="回复")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="发布时间")
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return self.content