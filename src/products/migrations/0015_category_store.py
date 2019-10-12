# Generated by Django 2.2.6 on 2019-10-12 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_permissions_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='store',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to='products.Store', verbose_name='store'),
        ),
    ]
