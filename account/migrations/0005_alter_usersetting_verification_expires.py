# Generated by Django 3.2.16 on 2023-01-12 16:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_user_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersetting',
            name='verification_expires',
            field=models.DateField(default=datetime.date(2023, 1, 15)),
        ),
    ]
