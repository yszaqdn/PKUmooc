from django.contrib import admin
from .models import Student, Teacher, Dept, User

# Register your models here.

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(User)
admin.site.register(Dept)
