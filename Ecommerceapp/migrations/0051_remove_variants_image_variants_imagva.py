# Generated by Django 4.2.7 on 2023-11-12 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerceapp', '0050_remove_variants_image_id_variants_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variants',
            name='image',
        ),
        migrations.AddField(
            model_name='variants',
            name='imagva',
            field=models.ImageField(null=True, upload_to='Product_images/Variant_images'),
        ),
    ]
