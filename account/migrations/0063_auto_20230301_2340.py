# Generated by Django 3.2.16 on 2023-03-01 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0062_alter_usersetting_verification_expires'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='user_membership',
        ),
        migrations.RemoveField(
            model_name='usermembership',
            name='membership',
        ),
        migrations.RemoveField(
            model_name='usermembership',
            name='user',
        ),
        migrations.DeleteModel(
            name='Membership',
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
        migrations.DeleteModel(
            name='UserMembership',
        ),
    ]
