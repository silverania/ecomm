# Generated by Django 4.0.1 on 2022-06-15 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default="media/images/user-secret-solid.svg')", null=True, upload_to='media/images/'),
        ),
    ]
