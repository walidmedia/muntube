# Generated by Django 3.2.16 on 2023-02-18 11:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0045_alter_usersetting_verification_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersetting',
            name='verification_expires',
            field=models.DateField(default=datetime.date(2023, 2, 21)),
        ),
    ]