from django.db import models
from datetime import datetime
from user_info.models import Teacher, Student
from django.utils import timezone
import uuid

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

    def __str__(self):
        return self.title

class Material(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="资料编号")
    title = models.CharField(max_length=50, verbose_name="资料标题")
    teacher = models.ForeignKey(to=Teacher, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="上传者")
    students = models.ManyToManyField(to=Student, verbose_name="已读学生")
    content = models.TextField(verbose_name="内容", blank=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, verbose_name="课程", related_name="materials")
    created_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False, verbose_name="是否公开")

    class Meta:
        ordering = ["-updated_time"]

    def __str__(self):
        return "%s : %s" %(self.course, self.title)


class Picture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID") # 32位uuid
    file_path = models.FileField(unique=True, upload_to = "uploads", verbose_name="路径")
    file_name = models.TextField(blank=True, verbose_name="文件名")
    created_time = models.DateTimeField(default=timezone.now, verbose_name="生成时间")
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="pictures")

    def __str__(self):
        return str(self.file_path)

    class Meta:
        ordering = ["-created_time"]
