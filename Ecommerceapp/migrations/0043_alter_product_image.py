# Generated by Django 4.2.7 on 2023-11-09 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerceapp', '0042_alter_banners_image_alter_brands_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='Product_images'),
        ),
    ]
