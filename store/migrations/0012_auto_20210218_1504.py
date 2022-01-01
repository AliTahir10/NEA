# Generated by Django 3.1.5 on 2021-02-18 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20210218_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('category', models.CharField(choices=[('Cake', 'Cake'), ('Cupcakes', 'Cupcakes'), ('DS', 'Dessert Shots'), ('Cakesicles', 'Cakesicles')], max_length=50, null=True)),
                ('minprice', models.FloatField(null=True)),
                ('Maxprice', models.FloatField(null=True)),
                ('picture', models.ImageField(upload_to='')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
    ]
