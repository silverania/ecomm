# Generated by Django 4.1.2 on 2023-07-17 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_remove_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
