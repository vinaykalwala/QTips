# Generated by Django 4.2.7 on 2023-11-12 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerceapp', '0057_alter_variants_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='variants',
            unique_together=set(),
        ),
    ]
