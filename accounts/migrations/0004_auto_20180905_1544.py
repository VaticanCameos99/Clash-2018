# Generated by Django 2.0.7 on 2018-09-05 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile_halt_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='halt_time',
            field=models.IntegerField(default=0),
        ),
    ]
