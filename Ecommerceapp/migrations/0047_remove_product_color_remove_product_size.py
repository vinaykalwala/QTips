# Generated by Django 4.2.7 on 2023-11-11 22:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerceapp', '0046_rename_images_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
    ]
