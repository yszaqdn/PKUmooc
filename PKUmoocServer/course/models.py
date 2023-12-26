from django.db import models
from datetime import datetime
from user_info.models import Teacher, Student

# Create your models here.

class Course(models.Model):
    id = models.CharField(max_length=20, primary_key=True, verbose_name="课程编号")
    title = models.CharField(max_length=50, verbose_name="课程名称")
    year = models.PositiveSmallIntegerField(verbose_name="学年", default=datetime.today().year) # type: ignore
    session = models.CharField(
        max_length=10, 
        choices = (("Spring", "春季"), ("Summer", "夏季"),
                   ("Fall", "秋季"), ("Winter", "冬季")),
        verbose_name="学期",
    )
    teachers = models.ManyToManyField(to=Teacher, verbose_name="授课教师")
    students = models.ManyToManyField(to=Student, verbose_name="选课学生")
