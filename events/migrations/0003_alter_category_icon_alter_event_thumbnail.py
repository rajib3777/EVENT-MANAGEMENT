# Generated by Django 5.2.4 on 2025-07-11 13:09

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_max_seats_alter_event_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='event',
            name='thumbnail',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]
