# Generated by Django 2.0.7 on 2018-09-20 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_userprofile_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='answer',
            field=models.IntegerField(default=0),
        ),
    ]