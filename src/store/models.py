from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class TaxRate(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('name'))
    tax_rate = models.DecimalField(default=0, max_digits=5, decimal_places=2, verbose_name=_('tax rate'))
    store = models.ForeignKey(
        'products.Store',
        default=1,
        on_delete=models.CASCADE,
        related_name='store_tax_rate',
        verbose_name=_('store'),
    )
