# Generated by Django 3.1.5 on 2021-02-18 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_auto_20210218_1504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product_id',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
