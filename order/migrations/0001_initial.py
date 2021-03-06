# Generated by Django 3.2 on 2022-05-12 08:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import order.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogue', '0008_auto_20220512_0141'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authority', models.CharField(blank=True, max_length=220, null=True, verbose_name='authority')),
                ('ref_id', models.CharField(blank=True, max_length=220, null=True, verbose_name='ref id')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'پرداخت نشده'), (1, 'پرداخت و سفارش ثبت شده'), (2, 'بسته بندی محصول'), (3, 'حمل کالا'), (4, 'تحویل داده شده')], verbose_name='status')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('user', models.ForeignKey(on_delete=models.SET(order.models.delete_user), related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='order')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.order', verbose_name='order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='catalogue.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'Order Item',
                'verbose_name_plural': 'Order Items',
            },
        ),
    ]
