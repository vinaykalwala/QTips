# Generated by Django 4.2.7 on 2023-11-09 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerceapp', '0045_remove_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='images',
            new_name='image',
        ),
    ]
