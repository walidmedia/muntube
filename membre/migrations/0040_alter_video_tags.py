# Generated by Django 3.2.16 on 2023-02-26 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0039_alter_video_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='tags',
            field=models.CharField(blank=True, default=False, max_length=512),
        ),
    ]
