# Generated by Django 2.2 on 2019-11-01 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=20, verbose_name='城市名'),
        ),
    ]
