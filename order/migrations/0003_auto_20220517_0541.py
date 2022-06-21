# Generated by Django 3.2 on 2022-05-17 05:41

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0008_auto_20220512_0141'),
        ('order', '0002_auto_20220512_0848'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='order',
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='orderitem',
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product_color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogue.productcolor', verbose_name='product color'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'پرداخت نشده'), (1, 'سفارش ثبت شده'), (2, 'بسته بندی محصول'), (3, 'حمل کالا'), (4, 'تحویل داده شده')], verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveSmallIntegerField(verbose_name='quantity'),
        ),
    ]
