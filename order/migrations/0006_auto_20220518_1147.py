# Generated by Django 3.2 on 2022-05-18 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_order_need_checkout'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_special',
            field=models.BooleanField(default=False, verbose_name='is special'),
        ),
        migrations.AddField(
            model_name='order',
            name='special_price',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='special price'),
        ),
    ]
