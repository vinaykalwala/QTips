# Generated by Django 4.2.5 on 2023-10-30 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerceapp', '0023_comment_image_comment_numeric_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/comment_images/'),
        ),
    ]
