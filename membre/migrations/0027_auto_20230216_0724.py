# Generated by Django 3.2.16 on 2023-02-16 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0026_comment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='contenue_18',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='video',
            name='signal',
            field=models.BooleanField(default=False),
        ),
    ]
