# Generated by Django 3.2.16 on 2023-01-17 10:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_alter_userabonn_chaine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersetting',
            name='verification_expires',
            field=models.DateField(default=datetime.date(2023, 1, 20)),
        ),
    ]