# Generated by Django 3.2.8 on 2021-12-12 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='subject',
            new_name='fullname',
        ),
    ]
