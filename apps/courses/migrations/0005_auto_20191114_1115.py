# Generated by Django 2.2 on 2019-11-14 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_is_classics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='is_classics',
            field=models.BooleanField(default=False, verbose_name='是否经典课程'),
        ),
    ]
