# Generated by Django 4.2.5 on 2023-10-07 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0008_remove_property_is_rent_remove_property_is_sell_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='address',
            field=models.CharField(blank=True, default=None, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='propertyImage'),
        ),
        migrations.AlterField(
            model_name='property',
            name='latitude',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='location',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='longitude',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='price_per_cent',
            field=models.BigIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='title',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='total_cent',
            field=models.BigIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='type',
            field=models.CharField(blank=True, choices=[('rent', 'rent'), ('sale', 'sale')], default=None, max_length=30, null=True),
        ),
    ]