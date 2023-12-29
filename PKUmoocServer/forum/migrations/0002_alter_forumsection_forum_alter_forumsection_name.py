# Generated by Django 4.2.7 on 2023-12-29 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumsection',
            name='forum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.forum', verbose_name='讨论区'),
        ),
        migrations.AlterField(
            model_name='forumsection',
            name='name',
            field=models.CharField(max_length=100, verbose_name='板块'),
        ),
    ]
