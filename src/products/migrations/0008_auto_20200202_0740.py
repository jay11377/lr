# Generated by Django 3.0.1 on 2020-02-02 07:40

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='title', unique=True),
        ),
    ]