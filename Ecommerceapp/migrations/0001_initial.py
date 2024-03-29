# Generated by Django 4.2.7 on 2023-11-13 21:17

import Ecommerceapp.models
import autoslug.fields
import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Brands",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Brand_name", models.CharField(max_length=100, null=True)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="Brand_images"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Categorie",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, null=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="Subcategory_images"
                    ),
                ),
                ("slug", models.SlugField(max_length=255, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Color",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=100, null=True)),
                ("name", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Contact",
            fields=[
                ("contact_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=200, null=True)),
                ("subject", models.CharField(max_length=500, null=True)),
                ("message", models.TextField(max_length=1000, null=True)),
                ("email", models.EmailField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Coupon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=200, null=True)),
                ("discount", models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Discount_deal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Main_categorie",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, null=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="Main_category_images"
                    ),
                ),
                ("slug", models.SlugField(max_length=255, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Moving_text",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=300, null=True)),
                (
                    "date",
                    models.DateTimeField(default=django.utils.timezone.now, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ordered_product", ckeditor.fields.RichTextField(null=True)),
                ("paid", models.BooleanField(default=False, null=True)),
                ("firstname", models.CharField(max_length=200, null=True)),
                ("lastname", models.CharField(max_length=200, null=True)),
                ("email", models.EmailField(max_length=90, null=True)),
                ("address", models.TextField(null=True)),
                ("city", models.CharField(max_length=100, null=True)),
                ("zip_code", models.CharField(max_length=100, null=True)),
                ("additional_info", models.TextField(null=True)),
                (
                    "date",
                    models.DateTimeField(default=django.utils.timezone.now, null=True),
                ),
                ("phone", models.CharField(max_length=20, null=True)),
                ("amount", models.CharField(max_length=100, null=True)),
                ("payment_id", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Partners",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, null=True)),
                ("image", models.ImageField(null=True, upload_to="")),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(blank=True, default="", max_length=500, null=True),
                ),
                ("name", models.CharField(max_length=500, null=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=Ecommerceapp.models.Product.get_upload_path,
                    ),
                ),
                ("total_quantity", models.IntegerField(null=True)),
                ("Availability", models.IntegerField(null=True)),
                ("price", models.FloatField(null=True)),
                ("Discount", models.IntegerField(null=True)),
                ("tax", models.FloatField(blank=True, null=True)),
                ("packing_cost", models.FloatField(blank=True, null=True)),
                ("Product_info", ckeditor.fields.RichTextField(null=True)),
                ("model_name", models.CharField(max_length=120, null=True)),
                ("Description", ckeditor.fields.RichTextField(null=True)),
                (
                    "Category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Ecommerceapp.categorie",
                    ),
                ),
            ],
            options={
                "db_table": "app_Product",
            },
        ),
        migrations.CreateModel(
            name="Section",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Size",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, null=True)),
                ("code", models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Variants",
            fields=[
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        blank=True,
                        editable=False,
                        null=True,
                        populate_from="title",
                        unique=True,
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "image_id",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=Ecommerceapp.models.Variants.get_upload_path,
                    ),
                ),
                ("quantity", models.IntegerField(default=1)),
                ("price", models.FloatField(default=0)),
                (
                    "id",
                    models.CharField(
                        editable=False, max_length=50, primary_key=True, serialize=False
                    ),
                ),
                (
                    "color",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="Ecommerceapp.color",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Ecommerceapp.product",
                    ),
                ),
                (
                    "size",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="Ecommerceapp.size",
                    ),
                ),
            ],
            options={
                "unique_together": {("slug", "product")},
            },
        ),
        migrations.CreateModel(
            name="Variant_image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        null=True,
                        upload_to=Ecommerceapp.models.Variant_image.get_upload_path,
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Ecommerceapp.product",
                    ),
                ),
                (
                    "variant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Ecommerceapp.variants",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Sub_categorie",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, null=True)),
                ("slug", models.SlugField(max_length=255, null=True, unique=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Ecommerceapp.categorie",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Sliders",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Image", models.ImageField(null=True, upload_to="slider_imgs")),
                ("Sale", models.IntegerField(null=True)),
                ("Brand_name", models.CharField(max_length=200, null=True)),
                ("Discount", models.IntegerField(null=True)),
                ("Description", models.CharField(max_length=100, null=True)),
                ("Link", models.CharField(max_length=2000, null=True)),
                (
                    "Discount_deal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Ecommerceapp.discount_deal",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product_image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(null=True, upload_to="Product_images")),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Ecommerceapp.product",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="Section",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="Ecommerceapp.section",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="Sub_category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="Ecommerceapp.sub_categorie",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="Tags",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="Ecommerceapp.tag",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="brand",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="Ecommerceapp.brands",
            ),
        ),
        migrations.CreateModel(
            name="Order_item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("product", models.CharField(max_length=200, null=True)),
                ("image", models.ImageField(null=True, upload_to="Order_item")),
                ("quantity", models.IntegerField(null=True)),
                ("price", models.CharField(max_length=150, null=True)),
                ("total", models.CharField(max_length=180, null=True)),
                (
                    "order",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Ecommerceapp.order",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Header_Icons",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Icon", models.CharField(max_length=200, null=True)),
                (
                    "Category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Ecommerceapp.categorie",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "numeric_rating",
                    models.IntegerField(
                        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="comment_images"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Ecommerceapp.product",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="categorie",
            name="main_category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="Ecommerceapp.main_categorie",
            ),
        ),
        migrations.CreateModel(
            name="Banners",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(null=True, upload_to="sm_banners")),
                ("Key_point_2", models.CharField(max_length=100, null=True)),
                ("Key_point_1", models.CharField(max_length=200, null=True)),
                ("Discount", models.IntegerField(blank=True, null=True)),
                ("Link", models.CharField(blank=True, max_length=2000, null=True)),
                (
                    "Discount_deal",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Ecommerceapp.discount_deal",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Ecommerceapp.categorie",
                    ),
                ),
                (
                    "section",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Ecommerceapp.section",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Additional_info",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("specification", models.CharField(max_length=120, null=True)),
                ("detail", models.CharField(max_length=100, null=True)),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Ecommerceapp.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Rating",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("stars", models.IntegerField()),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Ecommerceapp.product",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("product", "user")},
            },
        ),
    ]
