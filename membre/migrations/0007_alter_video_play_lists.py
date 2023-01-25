# Generated by Django 3.2.16 on 2023-01-25 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0030_alter_usersetting_verification_expires'),
        ('membre', '0006_alter_video_view_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='play_lists',
            field=models.ForeignKey(blank=True, default='NonClassifié', null=True, on_delete=django.db.models.deletion.CASCADE, to='account.playlist'),
        ),
    ]
