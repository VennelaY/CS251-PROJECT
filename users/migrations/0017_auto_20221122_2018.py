# Generated by Django 3.2.8 on 2022-11-22 20:18

from django.db import migrations, models
import users.decorators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20221122_1922'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='marks',
            new_name='assignment_marks',
        ),
        migrations.RenameField(
            model_name='assignment',
            old_name='title',
            new_name='assignment_name',
        ),
        migrations.RenameField(
            model_name='assignment',
            old_name='content',
            new_name='question_content',
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='question',
        ),
        migrations.AddField(
            model_name='assignment',
            name='related_file',
            field=models.FileField(null=True, upload_to='file1/', validators=[users.decorators.validate_file]),
        ),
    ]
