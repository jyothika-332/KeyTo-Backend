# Generated by Django 4.2.5 on 2023-09-24 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0005_user_otp_remove_user_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
