# Generated by Django 3.2.8 on 2021-12-08 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_order_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='country_code',
        ),
    ]
