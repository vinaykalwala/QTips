# Generated by Django 4.2.7 on 2023-11-12 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerceapp', '0053_variants_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variants',
            name='images',
        ),
        migrations.AddField(
            model_name='variants',
            name='image_id',
            field=models.ImageField(blank=True, null=True, upload_to='Product_images/Variant_images'),
        ),
    ]