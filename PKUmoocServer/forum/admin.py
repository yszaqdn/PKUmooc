from django.contrib import admin
from forum.models import DiscussionForum, ForumSection, Post, Reply

# Register your models here.
admin.site.register(DiscussionForum)
admin.site.register(ForumSection)
admin.site.register(Post)
admin.site.register(Reply)
