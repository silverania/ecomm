# Generated by Django 4.0.1 on 2022-06-15 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default="static/images/user-secret-solid.svg')", null=True, upload_to='../user/static/images/'),
        ),
    ]