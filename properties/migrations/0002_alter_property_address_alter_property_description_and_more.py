# Generated by Django 4.2.5 on 2023-09-21 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='address',
            field=models.CharField(default=None, max_length=250),
        ),
        migrations.AlterField(
            model_name='property',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='image',
            field=models.ImageField(default=None, upload_to=''),
        ),
        migrations.AlterField(
            model_name='property',
            name='is_rent',
            field=models.BooleanField(default=None),
        ),
        migrations.AlterField(
            model_name='property',
            name='is_sell',
            field=models.BooleanField(default=None),
        ),
        migrations.AlterField(
            model_name='property',
            name='location',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AlterField(
            model_name='property',
            name='price_per_cent',
            field=models.BigIntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='property',
            name='total_cent',
            field=models.BigIntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='property',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
