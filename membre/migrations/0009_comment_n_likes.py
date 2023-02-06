# Generated by Django 3.2.16 on 2023-01-27 23:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('membre', '0008_comment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='n_likes',
            field=models.ManyToManyField(blank=True, related_name='likes_comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
