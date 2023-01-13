# Generated by Django 3.2.16 on 2023-01-11 22:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0003_delete_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('contenue', models.TextField()),
                ('date_added', models.DateTimeField(default=datetime.datetime.today)),
            ],
        ),
    ]