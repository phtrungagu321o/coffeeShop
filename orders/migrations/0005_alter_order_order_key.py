# Generated by Django 3.2.8 on 2021-12-08 14:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_order_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_key',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]