# Generated by Django 4.2.7 on 2023-12-25 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_info", "0008_remove_dept_id_alter_dept_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="dept",
            field=models.CharField(max_length=50, verbose_name="学院名称"),
        ),
    ]