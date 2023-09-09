# Generated by Django 4.0.1 on 2022-08-12 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_manager_category_manager_product_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='manager',
            name='slug',
            field=models.SlugField(default='none', max_length=200, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='manager',
            name='name',
            field=models.CharField(db_index=True, max_length=200),
        ),
    ]
