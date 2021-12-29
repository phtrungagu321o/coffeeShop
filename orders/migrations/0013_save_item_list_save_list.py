# Generated by Django 3.2.8 on 2021-12-24 13:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_producttype_slug'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0012_alter_order_total_paid'),
    ]

    operations = [
        migrations.CreateModel(
            name='save_List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('total_paid', models.DecimalField(decimal_places=3, max_digits=8)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='save_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='save_Item_List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=3, max_digits=8)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='save_item', to='store.product')),
                ('save_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items_save_list', to='orders.save_list')),
            ],
            options={
                'ordering': ('save_list',),
            },
        ),
    ]