# Generated by Django 3.2.16 on 2023-02-05 14:07

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('membre', '0023_comment_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='soutien',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=10)),
                ('date_don', models.DateTimeField(default=datetime.datetime.today)),
                ('donneur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='donneur_soutien', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
