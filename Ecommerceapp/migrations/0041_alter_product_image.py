# Generated by Django 4.2.7 on 2023-11-09 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerceapp', '0040_alter_product_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='Product_images'),
        ),
    ]
