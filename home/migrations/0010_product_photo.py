# Generated by Django 4.2.4 on 2023-08-29 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='photo',
            field=models.ImageField(default='', upload_to='products'),
        ),
    ]