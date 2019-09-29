from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Category, Product, Store


# Register your models here.
class InlineProduct(admin.TabularInline):
    model = Product
    extra = 1


class StoreAdmin(ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


admin.site.register(Store, StoreAdmin)


class CategoryAdmin(ModelAdmin):
    inlines = [InlineProduct]


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(ModelAdmin):
    list_display = ('title', 'category')
    list_filter = ('category',)
    search_fields = ('title',)


admin.site.register(Product, ProductAdmin)
