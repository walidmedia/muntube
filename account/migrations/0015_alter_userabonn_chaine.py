# Generated by Django 3.2.16 on 2023-01-16 21:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_alter_userabonn_chaine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userabonn',
            name='chaine',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
