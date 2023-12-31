# Generated by Django 4.2.7 on 2023-11-09 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerceapp', '0041_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banners',
            name='image',
            field=models.ImageField(null=True, upload_to='sm_banners'),
        ),
        migrations.AlterField(
            model_name='brands',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='Brand_images'),
        ),
        migrations.AlterField(
            model_name='categorie',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='Subcategory_images'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='comment_images'),
        ),
        migrations.AlterField(
            model_name='main_categorie',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='Main_category_images'),
        ),
        migrations.AlterField(
            model_name='order_item',
            name='image',
            field=models.ImageField(null=True, upload_to='Order_item'),
        ),
        migrations.AlterField(
            model_name='sliders',
            name='Image',
            field=models.ImageField(null=True, upload_to='slider_imgs'),
        ),
    ]
