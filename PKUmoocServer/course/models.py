from django.db import models
from datetime import datetime

from django.db.models.fields.files import default_storage
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
    is_public = models.BooleanField(default=False, verbose_name="是否公开") # type: ignore

    class Meta:
        ordering = ["-updated_time"]

    def __str__(self):
        return "%s : %s" %(self.course, self.title)


class Picture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID") # 32位uuid
    file_path = models.FileField(unique=True, upload_to = "uploads", verbose_name="路径")
    file_name = models.TextField(blank=True, verbose_name="文件名")
    created_time = models.DateTimeField(default=timezone.now, verbose_name="生成时间")
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="pictures", verbose_name="课程材料")

    def __str__(self):
        return str(self.file_path)

    class Meta:
        ordering = ["-created_time"]


class Homework(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="作业编号")
    title = models.CharField(max_length=50, verbose_name="资料标题")
    teacher = models.ForeignKey(to=Teacher, on_delete=models.CASCADE, verbose_name="布置者")
    submit_begin_time = models.DateTimeField(default=timezone.now, verbose_name="开始提交时间")
    submit_end_time = models.DateTimeField(verbose_name="提交截止时间")
    view_begin_time = models.DateTimeField(default=timezone.now, verbose_name="开始可见时间")
    view_end_time = models.DateTimeField(verbose_name="最后可见时间")
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, related_name="homeworks", verbose_name="课程")

    def __str__(self):
        return "%s : %s" %(self.course, self.title)

    class Meta:
        ordering = ["-submit_end_time"]


class Problem(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="题目编号")
    description = models.TextField(verbose_name="题目描述")
    points = models.PositiveSmallIntegerField(verbose_name="分数")
    expected_answer = models.TextField(verbose_name="参考答案")
    teacher = models.ForeignKey(to=Teacher, verbose_name="上传者", on_delete=models.CASCADE)
    homework = models.ForeignKey(to=Homework, verbose_name="作业", on_delete=models.CASCADE, related_name="problems")

    @property
    def is_choice_problem(self):
        if hasattr(self, "choice"):
            return True
        return False

    def __str__(self):
        return "%s[P%d]" %(self.homework, self.id)

class Choice(models.Model):
    problem = models.OneToOneField(to=Problem, primary_key=True, on_delete=models.CASCADE, verbose_name="问题")
    choiceA = models.TextField(verbose_name="A")
    choiceB = models.TextField(verbose_name="B")
    choiceC = models.TextField(verbose_name="C")
    choiceD = models.TextField(verbose_name="D")
    is_multiple = models.BooleanField(default=False, verbose_name="是否多选") # type: ignore

    def __str__(self):
        return "%s-choices" % self.problem

class Submission(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="编号")
    student = models.ForeignKey(to=Student, verbose_name="提交者", on_delete=models.CASCADE)
    homework = models.ForeignKey(to=Homework, verbose_name="作业", on_delete=models.CASCADE)
    is_submitted = models.BooleanField(default=False, verbose_name="是否已提交") # type: ignore
    is_checked = models.BooleanField(default=False, verbose_name="是否已批改") # type: ignore
    score = models.SmallIntegerField(default=-1, verbose_name="成绩") # type: ignore
    remark = models.TextField(verbose_name="评语")

class Answer(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="编号")
    submission = models.ForeignKey(to=Submission, verbose_name="提交", on_delete=models.CASCADE)
    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE, verbose_name="问题")
    content = models.TextField(verbose_name="回答")
    score = models.SmallIntegerField(verbose_name="得分", default=-1) # type: ignore

    class Meta:
        unique_together = ["submission", "problem"]
