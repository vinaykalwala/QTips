# Generated by Django 4.2.7 on 2023-11-13 01:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Ecommerceapp', '0065_remove_cartitem_cart_remove_cartitem_variant_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('variant_title', models.CharField(blank=True, max_length=100)),
                ('variant_price', models.FloatField(null=True)),
                ('variant_image', models.ImageField(blank=True, null=True, upload_to='Cart_images')),
                ('variant_size', models.CharField(blank=True, max_length=50)),
                ('variant_color', models.CharField(blank=True, max_length=50)),
                ('product_id', models.IntegerField(default=0)),
                ('packing_cost', models.FloatField(default=1)),
                ('tax', models.FloatField(default=1)),
                ('model_name', models.CharField(default='Model name', max_length=120)),
                ('brand_name', models.CharField(default='default_brand_value', max_length=50)),
                ('tag_name', models.CharField(default='Tag name', max_length=50)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='CART.cart')),
                ('variant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Ecommerceapp.variants')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(related_name='cart_items', to='CART.cartitem'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
