# Generated by Django 3.2.8 on 2022-11-25 01:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_auto_20221124_2155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='duration',
        ),
        migrations.AddField(
            model_name='assignment',
            name='deadline',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='filemodel',
            name='file',
            field=models.FileField(default='', upload_to='f'),
        ),
    ]