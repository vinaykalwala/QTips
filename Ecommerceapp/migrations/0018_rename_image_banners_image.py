# Generated by Django 4.2.5 on 2023-10-13 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerceapp', '0017_rename_image_banner_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banners',
            old_name='Image',
            new_name='image',
        ),
    ]
