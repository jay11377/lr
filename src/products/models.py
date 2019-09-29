from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Store(models.Model):
    title = models.CharField(max_length=200)
    domain = models.CharField(max_length=200)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='store',
        verbose_name=_('owner'),
    )

    class Meta:
        verbose_name = _('store')
        verbose_name_plural = _('stores')

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        get_user_model(),
        default=1,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='plats',
        verbose_name=_('category'),
    )
    title = models.CharField(max_length=200)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    photo = models.ImageField(null=True, upload_to='products')

    class Meta:
        verbose_name = _('plat')
        verbose_name_plural = _('plats')

    def __str__(self):
        return self.title
