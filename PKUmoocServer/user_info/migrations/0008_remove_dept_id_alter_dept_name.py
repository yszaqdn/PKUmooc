# Generated by Django 4.2.7 on 2023-12-24 11:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_info", "0007_remove_teacher_id_alter_teacher_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dept",
            name="id",
        ),
        migrations.AlterField(
            model_name="dept",
            name="name",
            field=models.CharField(
                max_length=50, primary_key=True, serialize=False, verbose_name="学院名称"
            ),
        ),
    ]
