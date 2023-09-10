# Generated by Django 4.0.1 on 2022-08-12 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='manager',
            field=models.ManyToManyField(to='home.Manager'),
        ),
        migrations.AddField(
            model_name='product',
            name='manager',
            field=models.ManyToManyField(to='home.Manager'),
        ),
    ]