# Generated by Django 4.2.7 on 2023-12-28 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("user_info", "0011_delete_dept"),
        ("course", "0002_alter_picture_material_homework"),
    ]

    operations = [
        migrations.CreateModel(
            name="Problem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="题目编号"
                    ),
                ),
                ("description", models.TextField(verbose_name="题目描述")),
                ("points", models.PositiveSmallIntegerField(verbose_name="分数")),
                ("expected_answer", models.TextField(verbose_name="参考答案")),
                (
                    "homework",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="problems",
                        to="course.homework",
                        verbose_name="作业",
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user_info.teacher",
                        verbose_name="上传者",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Choice",
            fields=[
                (
                    "problem",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="course.problem",
                        verbose_name="问题",
                    ),
                ),
                ("choiceA", models.TextField(verbose_name="A")),
                ("choiceB", models.TextField(verbose_name="B")),
                ("choiceC", models.TextField(verbose_name="C")),
                ("choiceD", models.TextField(verbose_name="D")),
                (
                    "is_multiple",
                    models.BooleanField(default=False, verbose_name="是否多选"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Submission",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="编号"
                    ),
                ),
                (
                    "is_submitted",
                    models.BooleanField(default=False, verbose_name="是否已提交"),
                ),
                (
                    "is_checked",
                    models.BooleanField(default=False, verbose_name="是否已批改"),
                ),
                ("score", models.SmallIntegerField(default=-1, verbose_name="成绩")),
                ("remark", models.TextField(verbose_name="评语")),
                (
                    "homework",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.homework",
                        verbose_name="作业",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user_info.student",
                        verbose_name="提交者",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Answer",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="编号"
                    ),
                ),
                ("content", models.TextField(verbose_name="回答")),
                ("score", models.SmallIntegerField(default=-1, verbose_name="得分")),
                (
                    "problem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.problem",
                        verbose_name="问题",
                    ),
                ),
                (
                    "submission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.submission",
                        verbose_name="提交",
                    ),
                ),
            ],
            options={
                "unique_together": {("submission", "problem")},
            },
        ),
    ]
