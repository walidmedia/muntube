# Generated by Django 3.2.16 on 2023-02-19 14:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0046_alter_usersetting_verification_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersetting',
            name='verification_expires',
            field=models.DateField(default=datetime.date(2023, 2, 22)),
        ),
    ]
