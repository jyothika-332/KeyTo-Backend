# Generated by Django 4.2.5 on 2023-09-20 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_alter_user_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.BigIntegerField(default=2),
            preserve_default=False,
        ),
    ]