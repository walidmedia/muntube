# Generated by Django 3.2.16 on 2023-02-27 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0040_alter_video_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='miniature',
            field=models.ImageField(blank=True, default='/static/images/Playlist non classée.svg', null=True, upload_to='imagevid'),
        ),
    ]
