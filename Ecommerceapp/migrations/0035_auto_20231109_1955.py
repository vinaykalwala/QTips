# Generated by Django 3.0.14 on 2023-11-09 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerceapp', '0034_auto_20231109_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='name',
            field=models.CharField(default='black', max_length=20),
        ),
    ]
