# Generated by Django 3.2.16 on 2023-01-28 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0009_comment_n_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
