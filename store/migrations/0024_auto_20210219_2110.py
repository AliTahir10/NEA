# Generated by Django 3.1.5 on 2021-02-19 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_auto_20210219_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
