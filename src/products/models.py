from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Store(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('title'))
    domain = models.CharField(max_length=200, verbose_name=_('domain'))
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
    title = models.CharField(max_length=200, verbose_name=_('title'))
    author = models.ForeignKey(
        get_user_model(),
        default=1,
        on_delete=models.CASCADE,
        verbose_name=_('author'),
        editable=False,
    )
    store = models.ForeignKey(
        Store,
        default=1,
        on_delete=models.CASCADE,
        related_name=_('store'),
        verbose_name=_('store'),
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
        related_name='dish',
        verbose_name=_('category'),
    )
    title = models.CharField(max_length=200, verbose_name=_('title'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2, verbose_name=_('price'))
    photo = models.ImageField(null=True, upload_to='products', verbose_name=_('photo'))
    spicy = models.BooleanField(default=False, verbose_name=_('spicy'))
    vegetarian = models.BooleanField(default=False, verbose_name=_('vegetarian'))

    class Meta:
        verbose_name = _('dish')
        verbose_name_plural = _('dishes')

    def __str__(self):
        return self.title
