# Generated by Django 4.2.7 on 2023-11-13 00:30

import Ecommerceapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerceapp', '0062_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variants',
            name='image_id',
            field=models.ImageField(blank=True, null=True, upload_to=Ecommerceapp.models.Variants.get_upload_path),
        ),
    ]
