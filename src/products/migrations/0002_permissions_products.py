# Generated by Django 3.0.1 on 2020-01-28 10:12

from django.db import migrations
from django.contrib.auth.models import Group, Permission


def create_permissions(apps, schema_editor):
    group, created = Group.objects.get_or_create(name="Restaurant")

    group.permissions.add(
        # Category
        Permission.objects.get(codename='add_category'),
        Permission.objects.get(codename='change_category'),
        Permission.objects.get(codename='delete_category'),
        Permission.objects.get(codename='view_category'),

        # Product
        Permission.objects.get(codename='add_product'),
        Permission.objects.get(codename='change_product'),
        Permission.objects.get(codename='delete_product'),
        Permission.objects.get(codename='view_product'),

        # Tax Rate
        Permission.objects.get(codename='add_taxrate'),
        Permission.objects.get(codename='change_taxrate'),
        Permission.objects.get(codename='delete_taxrate'),
        Permission.objects.get(codename='view_taxrate'),

        # Delivery Area
        Permission.objects.get(codename='add_deliveryarea'),
        Permission.objects.get(codename='change_deliveryarea'),
        Permission.objects.get(codename='delete_deliveryarea'),
        Permission.objects.get(codename='view_deliveryarea'),

        # Delivery City
        Permission.objects.get(codename='add_deliverycity'),
        Permission.objects.get(codename='change_deliverycity'),
        Permission.objects.get(codename='delete_deliverycity'),
        Permission.objects.get(codename='view_deliverycity'),

        # Menu
        Permission.objects.get(codename='add_menu'),
        Permission.objects.get(codename='change_menu'),
        Permission.objects.get(codename='delete_menu'),
        Permission.objects.get(codename='view_menu'),

        # Menu Option
        Permission.objects.get(codename='add_menuoption'),
        Permission.objects.get(codename='change_menuoption'),
        Permission.objects.get(codename='delete_menuoption'),
        Permission.objects.get(codename='view_menuoption'),

        # Menu Option Product
        Permission.objects.get(codename='add_menuoptionproduct'),
        Permission.objects.get(codename='change_menuoptionproduct'),
        Permission.objects.get(codename='delete_menuoptionproduct'),
        Permission.objects.get(codename='view_menuoptionproduct'),
    )


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_permissions, reverse_code=lambda *args, **kwargs: True)
    ]
