# Generated by Django 4.2.5 on 2023-10-13 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerceapp', '0015_remove_product_cart_sm_banner_category_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Sm_Banner',
            new_name='Banners',
        ),
    ]
