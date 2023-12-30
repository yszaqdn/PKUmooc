from django.contrib import admin
from course.models import Course, Material, Picture, Homework, Problem, Choice, Submission, Answer, Post, ForumSection, Reply

# Register your models here.

admin.site.register(Course)
admin.site.register(Material)
admin.site.register(Picture)
admin.site.register(Homework)
admin.site.register(Problem)
admin.site.register(Answer)
admin.site.register(Submission)
admin.site.register(Choice)
admin.site.register(Post)
admin.site.register(ForumSection)
admin.site.register(Reply)
