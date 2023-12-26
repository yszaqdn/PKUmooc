# Generated by Django 4.2.7 on 2023-12-26 03:17

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("user_info", "0008_remove_dept_id_alter_dept_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.CharField(
                        max_length=20,
                        primary_key=True,
                        serialize=False,
                        verbose_name="课程编号",
                    ),
                ),
                ("title", models.CharField(max_length=50, verbose_name="课程名称")),
                (
                    "year",
                    models.PositiveSmallIntegerField(default=2023, verbose_name="学年"),
                ),
                (
                    "session",
                    models.CharField(
                        choices=[
                            ("Spring", "春季"),
                            ("Summer", "夏季"),
                            ("Fall", "秋季"),
                            ("Winter", "冬季"),
                        ],
                        max_length=10,
                        verbose_name="学期",
                    ),
                ),
                (
                    "students",
                    models.ManyToManyField(to="user_info.student", verbose_name="选课学生"),
                ),
                (
                    "teachers",
                    models.ManyToManyField(to="user_info.teacher", verbose_name="授课教师"),
                ),
            ],
        ),
    ]
