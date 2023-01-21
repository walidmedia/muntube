# Generated by Django 3.2.16 on 2023-01-21 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0028_auto_20230121_1221'),
        ('membre', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='play_lists',
            field=models.ForeignKey(blank=True, default=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.playlist'),
        ),
        migrations.AlterField(
            model_name='video',
            name='status_video',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
