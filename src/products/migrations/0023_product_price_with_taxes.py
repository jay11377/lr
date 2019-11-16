# Generated by Django 2.2.6 on 2019-11-06 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_add_categoy_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_with_taxes',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='price'),
        ),
    ]