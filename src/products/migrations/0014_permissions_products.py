# Generated by Django 2.2.6 on 2019-10-12 09:44

from django.db import migrations
from django.contrib.auth.models import Group, Permission


def create_permissions(apps, schema_editor):
    group = Group.objects.get(name="Restaurant")

    group.permissions.add(
        Permission.objects.get(codename='add_product'),
        Permission.objects.get(codename='change_product'),
        Permission.objects.get(codename='delete_product'),
        Permission.objects.get(codename='view_product'),
    )


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20191012_1008'),
    ]

    operations = [
        migrations.RunPython(create_permissions, reverse_code=lambda *args, **kwargs: True)
    ]