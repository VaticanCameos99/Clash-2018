# Generated by Django 2.0.7 on 2018-09-20 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20180920_0507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mcq',
            name='question',
            field=models.TextField(default=' ', max_length=150),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]
