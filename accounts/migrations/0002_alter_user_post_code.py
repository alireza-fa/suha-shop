# Generated by Django 3.2 on 2022-05-13 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='post_code',
            field=models.PositiveBigIntegerField(blank=True, null=True, verbose_name='post code'),
        ),
    ]
