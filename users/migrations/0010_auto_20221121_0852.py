# Generated by Django 3.2.12 on 2022-11-21 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='end_date',
        ),
        migrations.AddField(
            model_name='course',
            name='course_code',
            field=models.CharField(default=3, max_length=100),
            preserve_default=False,
        ),
    ]
