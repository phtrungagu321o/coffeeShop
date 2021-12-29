# Generated by Django 3.2.8 on 2021-12-13 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryoptions',
            name='delivery_price',
            field=models.DecimalField(decimal_places=3, error_messages={'name': {'max_length': 'The price must be between 0 and 99999.999'}}, help_text='Maximum 1.000.000', max_digits=8, verbose_name='delivery price'),
        ),
    ]