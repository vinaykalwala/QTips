# Generated by Django 4.2.5 on 2023-10-13 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerceapp', '0012_alter_order_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='additional_info',
            name='product',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='Discount_deal',
        ),
        migrations.RemoveField(
            model_name='categorie',
            name='main_category',
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.DeleteModel(
            name='Coupon',
        ),
        migrations.DeleteModel(
            name='Moving_text',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.RemoveField(
            model_name='order_item',
            name='order',
        ),
        migrations.DeleteModel(
            name='OrderUpdate',
        ),
        migrations.DeleteModel(
            name='Partners',
        ),
        migrations.RemoveField(
            model_name='product',
            name='Category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='Section',
        ),
        migrations.RemoveField(
            model_name='product',
            name='Sub_category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='Tags',
        ),
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.RemoveField(
            model_name='product_image',
            name='product',
        ),
        migrations.RemoveField(
            model_name='sliders',
            name='Discount_deal',
        ),
        migrations.RemoveField(
            model_name='sm_banner',
            name='Discount_deal',
        ),
        migrations.RemoveField(
            model_name='sub_categorie',
            name='category',
        ),
        migrations.DeleteModel(
            name='Additional_info',
        ),
        migrations.DeleteModel(
            name='Banner',
        ),
        migrations.DeleteModel(
            name='Brands',
        ),
        migrations.DeleteModel(
            name='Categorie',
        ),
        migrations.DeleteModel(
            name='Color',
        ),
        migrations.DeleteModel(
            name='Discount_deal',
        ),
        migrations.DeleteModel(
            name='Main_categorie',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Order_item',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='Product_image',
        ),
        migrations.DeleteModel(
            name='Section',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
        migrations.DeleteModel(
            name='Sliders',
        ),
        migrations.DeleteModel(
            name='Sm_Banner',
        ),
        migrations.DeleteModel(
            name='Sub_categorie',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]