# Generated by Django 3.2.8 on 2022-11-22 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_assignment_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsubmission',
            name='Title',
            field=models.CharField(default='00000', max_length=100),
        ),
    ]
