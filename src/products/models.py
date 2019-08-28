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
