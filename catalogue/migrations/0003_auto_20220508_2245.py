# Generated by Django 3.2 on 2022-05-08 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_alter_product_brand'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boxproduct',
            name='product',
        ),
        migrations.AddField(
            model_name='boxproduct',
            name='product',
            field=models.ManyToManyField(related_name='boxes', to='catalogue.Product', verbose_name='boxes'),
        ),
    ]
