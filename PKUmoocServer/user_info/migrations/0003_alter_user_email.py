# Generated by Django 4.2.7 on 2023-12-21 17:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_info", "0002_remove_student_id_alter_dept_name_alter_student_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, verbose_name="email address"),
        ),
    ]
