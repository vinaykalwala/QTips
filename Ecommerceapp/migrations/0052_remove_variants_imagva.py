# Generated by Django 4.2.7 on 2023-11-12 03:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerceapp', '0051_remove_variants_image_variants_imagva'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variants',
            name='imagva',
        ),
    ]