# Generated by Django 4.2.5 on 2023-10-13 05:35

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Ecommerceapp', '0013_remove_additional_info_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Brand_name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/Brand_images')),
            ],
        ),
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/Subcategory_images')),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('contact_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=500)),
                ('message', models.TextField(max_length=1000)),
                ('email', models.EmailField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=200)),
                ('discount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Discount_deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Main_categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/Main_category_images')),
            ],
        ),
        migrations.CreateModel(
            name='Moving_text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_product', ckeditor.fields.RichTextField(null=True)),
                ('paid', models.BooleanField(default=False, null=True)),
                ('firstname', models.CharField(max_length=200)),
                ('lastname', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=90)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=100)),
                ('additional_info', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('phone', models.CharField(max_length=20)),
                ('amount', models.CharField(max_length=100)),
                ('payment_id', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderUpdate',
            fields=[
                ('update_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_id', models.IntegerField(default='')),
                ('update_desc', models.CharField(max_length=5000)),
                ('delivered', models.BooleanField(default=False)),
                ('timestamp', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Partners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, default='', max_length=500, null=True)),
                ('name', models.CharField(max_length=120)),
                ('image', models.ImageField(upload_to='media/Product_images')),
                ('total_quantity', models.IntegerField()),
                ('Availability', models.IntegerField()),
                ('price', models.FloatField()),
                ('Discount', models.IntegerField()),
                ('tax', models.FloatField(blank=True, null=True)),
                ('packing_cost', models.FloatField(blank=True, null=True)),
                ('Product_info', ckeditor.fields.RichTextField()),
                ('model_name', models.CharField(max_length=120)),
                ('Description', ckeditor.fields.RichTextField()),
                ('cart', models.BooleanField(default=False)),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ecommerceapp.categorie')),
            ],
            options={
                'db_table': 'app_Product',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Sub_categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ecommerceapp.categorie')),
            ],
        ),
        migrations.CreateModel(
            name='Sm_Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(upload_to='media/sm_banners')),
                ('Key_point_2', models.CharField(max_length=200)),
                ('Discount', models.IntegerField()),
                ('Link', models.CharField(max_length=2000)),
                ('Discount_deal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ecommerceapp.discount_deal')),
            ],
        ),
        migrations.CreateModel(
            name='Sliders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(upload_to='media/slider_imgs')),
                ('Sale', models.IntegerField()),
                ('Brand_name', models.CharField(max_length=200)),
                ('Discount', models.IntegerField()),
                ('Description', models.CharField(max_length=100)),
                ('Link', models.CharField(max_length=2000)),
                ('Discount_deal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ecommerceapp.discount_deal')),
            ],
        ),
        migrations.CreateModel(
            name='Product_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=120)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ecommerceapp.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='Section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Ecommerceapp.section'),
        ),
        migrations.AddField(
            model_name='product',
            name='Sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Ecommerceapp.sub_categorie'),
        ),
        migrations.AddField(
            model_name='product',
            name='Tags',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Ecommerceapp.tag'),
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Ecommerceapp.brands'),
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Ecommerceapp.color'),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Ecommerceapp.size'),
        ),
        migrations.CreateModel(
            name='Order_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='images/Order_item')),
                ('quantity', models.IntegerField()),
                ('price', models.CharField(max_length=150)),
                ('total', models.CharField(max_length=180)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ecommerceapp.order')),
            ],
        ),
        migrations.AddField(
            model_name='categorie',
            name='main_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ecommerceapp.main_categorie'),
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(upload_to='media/Banner_imgs')),
                ('Sale', models.IntegerField()),
                ('Brand_name', models.CharField(max_length=200)),
                ('Discount', models.IntegerField()),
                ('Description', models.CharField(max_length=100)),
                ('Link', models.CharField(max_length=2000)),
                ('Discount_deal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ecommerceapp.discount_deal')),
            ],
        ),
        migrations.CreateModel(
            name='Additional_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specification', models.CharField(max_length=120)),
                ('detail', models.CharField(max_length=100)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ecommerceapp.product')),
            ],
        ),
    ]
