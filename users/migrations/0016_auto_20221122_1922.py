# Generated by Django 3.2.8 on 2022-11-22 19:22

from django.db import migrations, models
import users.decorators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20221122_1811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='created_at',
        ),
        migrations.AddField(
            model_name='assignment',
            name='question',
            field=models.FileField(null=True, upload_to='file1/', validators=[users.decorators.validate_file], verbose_name=''),
        ),
    ]
