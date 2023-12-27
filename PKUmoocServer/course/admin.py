from django.contrib import admin
from course.models import Course, Material, Picture, Homework

# Register your models here.

admin.site.register(Course)
admin.site.register(Material)
admin.site.register(Picture)
admin.site.register(Homework)
