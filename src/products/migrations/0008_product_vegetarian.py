# Generated by Django 2.2.6 on 2019-10-09 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_product_spicy'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='vegetarian',
            field=models.BooleanField(default=False),
        ),
    ]