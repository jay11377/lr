from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import TaxRate

# Register your models here.


class TaxRateAdmin(ModelAdmin):
    list_display = ('name', 'tax_rate', 'store')


admin.site.register(TaxRate, TaxRateAdmin)
