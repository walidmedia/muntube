# Generated by Django 3.2.16 on 2023-02-28 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0059_auto_20230228_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
