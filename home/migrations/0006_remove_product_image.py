# Generated by Django 4.1.2 on 2023-05-26 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]