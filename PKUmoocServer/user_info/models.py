from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.


class User(AbstractUser):
    # @property is something like an attribute, e.g.
    # >>> u.is_student  # if User u is student
    # True
    #
    # Also, use reverse search to get the role related information
    # e.g.  use u.student.id to get the student's id
    # instead of user.id, and also for the other attributes.
    @property
    def is_student(self):
        if hasattr(self, "student"):
            return True
        return False

    @property
    def is_teacher(self):
        if hasattr(self, "teacher"):
            return True
        return False


class Dept(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="学院编号")
    name = models.CharField(max_length=200, verbose_name="学院名称")

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.CharField(
        primary_key=True,
        max_length=10,
        verbose_name="学号",
    )
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, verbose_name="学院")
    name = models.CharField(max_length=50, verbose_name="姓名")
    sex = models.CharField(
        max_length=6, 
        choices=(("Male", "男"), ("Female", "女")), 
        default="Male",
        verbose_name="性别",
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="电话",
    )
    grade = models.PositiveSmallIntegerField(
        default=datetime.today().year, # 用四位年份表示
        verbose_name="年级"
    )
    # email and password is included in User class,
    # please reverse search to get them
    # e.g. student.user.email

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.CharField(
        primary_key=True,
        max_length=10,
        verbose_name="工号",
    )
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, verbose_name="学院")
    name = models.CharField(max_length=50, verbose_name="姓名")
    sex = models.CharField(
        max_length=6, 
        choices=(("Male", "男"), ("Female", "女")), 
        default="Male",
        verbose_name="性别",
    )
    phone = models.CharField(
        max_length=11,
        verbose_name="电话",
    )
    # email and password is included in User class,
    # please reverse search to get them

    def __str__(self):
        return self.name
