# Generated by Django 2.2.6 on 2019-10-16 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_product_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(to='products.Category', verbose_name='categories'),
        ),
    ]