# Generated by Django 4.2.7 on 2023-11-09 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerceapp', '0039_alter_product_color_alter_product_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_image',
            name='image',
            field=models.ImageField(null=True, upload_to='Product_images'),
        ),
    ]
