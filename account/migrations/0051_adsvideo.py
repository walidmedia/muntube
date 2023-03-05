# Generated by Django 3.2.16 on 2023-02-24 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0050_alter_usersetting_verification_expires'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdsVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('detail', models.TextField()),
                ('video', models.FileField(blank=True, upload_to='videosAds')),
                ('miniature', models.ImageField(blank=True, null=True, upload_to='imagevidAds')),
            ],
        ),
    ]