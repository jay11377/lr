from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=200)

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

    class Meta:
        verbose_name = _('plat')
        verbose_name_plural = _('plats')

    def __str__(self):
        return self.title
