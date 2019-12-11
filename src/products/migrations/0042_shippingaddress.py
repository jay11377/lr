# Generated by Django 2.2.7 on 2019-12-07 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0041_auto_20191207_1326'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_title', models.CharField(max_length=200, verbose_name='address title')),
                ('company', models.CharField(max_length=200, verbose_name='company')),
                ('address_first_name', models.CharField(max_length=200, verbose_name='first name')),
                ('address_last_name', models.CharField(max_length=200, verbose_name='last name')),
                ('address', models.CharField(max_length=200, verbose_name='address')),
                ('address_2', models.CharField(max_length=200, verbose_name='address (2)')),
                ('zip_code', models.CharField(max_length=200, verbose_name='zip code')),
                ('city', models.CharField(max_length=200, verbose_name='city')),
                ('phone', models.CharField(max_length=200, verbose_name='phone')),
                ('entrance_code', models.CharField(max_length=200, verbose_name='entrance code')),
                ('intercom', models.CharField(max_length=200, verbose_name='intercom')),
                ('stairs', models.CharField(max_length=200, verbose_name='stairs')),
                ('floor', models.CharField(max_length=200, verbose_name='floor')),
                ('apartment_number', models.CharField(max_length=200, verbose_name='apartment number')),
                ('comment', models.CharField(max_length=200, verbose_name='comment')),
            ],
            options={
                'verbose_name': 'shipping address',
                'verbose_name_plural': 'shipping addresses',
            },
        ),
    ]
