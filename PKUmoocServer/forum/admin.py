from django.contrib import admin
from forum.models import Forum, ForumSection, Post, Reply

# Register your models here.
admin.site.register(Forum)
admin.site.register(ForumSection)
admin.site.register(Post)
admin.site.register(Reply)
