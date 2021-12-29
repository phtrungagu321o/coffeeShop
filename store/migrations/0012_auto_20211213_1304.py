# Generated by Django 3.2.8 on 2021-12-13 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_product_regular_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_price',
            field=models.DecimalField(decimal_places=3, error_messages={'name': {'max_length': 'Giảm từ 0 đến 99999.999'}}, help_text='Tối đa 99999.999', max_digits=8, verbose_name='Discount price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='regular_price',
            field=models.DecimalField(decimal_places=3, error_messages={'name': {'max_length': 'Giá sản phẩm phải từ 0 đến 99999.999'}}, help_text='Tối đa 99999.999', max_digits=8, verbose_name='Regular price'),
        ),
    ]