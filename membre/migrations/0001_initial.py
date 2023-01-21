# Generated by Django 3.2.16 on 2023-01-20 14:08

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0024_playlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo_img', models.ImageField(upload_to='static/app_logos')),
            ],
        ),
        migrations.CreateModel(
            name='Banners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='banners/')),
                ('alt_text', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'Banners',
            },
        ),
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=150)),
                ('detail', models.TextField()),
                ('send_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quest', models.TextField()),
                ('ans', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('detail', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('detail', models.TextField()),
                ('img', models.ImageField(null=True, upload_to='static/services')),
            ],
        ),
        migrations.CreateModel(
            name='SubPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('price', models.IntegerField()),
                ('max_member', models.IntegerField(null=True)),
                ('highlight_status', models.BooleanField(default=False, null=True)),
                ('validity_days', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100, null=True)),
                ('pwd', models.CharField(max_length=50, null=True)),
                ('mobile', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('is_active', models.BooleanField(default=False)),
                ('detail', models.TextField()),
                ('img', models.ImageField(upload_to='static/trainers')),
                ('salary', models.IntegerField(default=0)),
                ('facebook', models.CharField(max_length=200, null=True)),
                ('twitter', models.CharField(max_length=200, null=True)),
                ('pinterest', models.CharField(max_length=200, null=True)),
                ('youtube', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrainerNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notif_msg', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('detail', models.TextField()),
                ('vid', models.FileField(blank=True, upload_to='videos')),
                ('miniature', models.ImageField(blank=True, null=True, upload_to='imagevid')),
                ('categorie', models.CharField(blank=True, default=False, max_length=150)),
                ('tags', models.CharField(blank=True, default=False, max_length=150)),
                ('status_video', models.IntegerField(default=0, null=True)),
                ('link', models.TextField(blank=True, null=True)),
                ('documents', models.FileField(blank=True, null=True, upload_to='filesvideo')),
                ('date_created', models.DateTimeField(default=datetime.datetime.today)),
                ('n_comments', models.ManyToManyField(blank=True, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('n_likes', models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('play_lists', models.ForeignKey(blank=True, default=False, on_delete=django.db.models.deletion.CASCADE, to='account.playlist')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TrainerSubscriberReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_msg', models.TextField()),
                ('report_for_trainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report_for_trainer', to='membre.trainer')),
                ('report_for_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report_for_user', to=settings.AUTH_USER_MODEL)),
                ('report_from_trainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report_from_trainer', to='membre.trainer')),
                ('report_from_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report_from_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TrainerSalary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amt', models.IntegerField()),
                ('amt_date', models.DateField()),
                ('remarks', models.TextField(blank=True)),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membre.trainer')),
            ],
            options={
                'verbose_name_plural': 'Trainer Salary',
            },
        ),
        migrations.CreateModel(
            name='TrainerMsg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('trainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='membre.trainer')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Messages For Trainer',
            },
        ),
        migrations.CreateModel(
            name='TrainerAchivement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('detail', models.TextField()),
                ('img', models.ImageField(upload_to='static/trainers_achivements')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membre.trainer')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(max_length=50)),
                ('reg_date', models.DateField(auto_now_add=True, null=True)),
                ('plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='membre.subplan')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('img', models.ImageField(null=True, upload_to='static/subs')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubPlanFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('subplan', models.ManyToManyField(to='membre.SubPlan')),
            ],
        ),
        migrations.CreateModel(
            name='savedvideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='membre.video')),
            ],
        ),
        migrations.CreateModel(
            name='PlanDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_months', models.IntegerField()),
                ('total_discount', models.IntegerField()),
                ('subplan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='membre.subplan')),
            ],
        ),
        migrations.CreateModel(
            name='Notify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notify_detail', models.TextField()),
                ('read_by_trainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='membre.trainer')),
                ('read_by_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NotifUserStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('notif', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membre.notify')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Notification Status',
            },
        ),
        migrations.CreateModel(
            name='NotifTrainerStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('notif', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membre.trainernotification')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membre.trainer')),
            ],
            options={
                'verbose_name_plural': 'Trainer Notification Status',
            },
        ),
        migrations.CreateModel(
            name='GalleryVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alt_text', models.CharField(max_length=150)),
                ('vid', models.FileField(null=True, upload_to='static/gallery_videos')),
                ('video', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='membre.video')),
            ],
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('contenue', models.TextField()),
                ('date_added', models.DateTimeField(default=datetime.datetime.today)),
                ('video', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='membre.video')),
            ],
        ),
        migrations.CreateModel(
            name='AssignSubscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membre.trainer')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
