# Generated by Django 4.2.5 on 2023-10-28 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_message_priority'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='priority',
        ),
    ]
