# Generated by Django 3.2.16 on 2023-02-27 10:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0057_alter_user_id_youtube_ch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersetting',
            name='verification_expires',
            field=models.DateField(default=datetime.date(2023, 3, 2)),
        ),
    ]
