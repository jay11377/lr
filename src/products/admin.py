from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Category, Product, Store


class FilterUserAdmin(ModelAdmin):
    # Force current user as author
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

    # Filter view with author = current user
    def get_queryset(self, request):
        qs = super(FilterUserAdmin, self).get_queryset(request)
        return qs.filter(author=request.user)


# Register your models here.
class InlineProduct(admin.TabularInline):
    model = Product
    extra = 1


class StoreAdmin(ModelAdmin):
    list_display = ('title', 'owner')
    search_fields = ('title',)


admin.site.register(Store, StoreAdmin)


class CategoryAdmin(FilterUserAdmin):
    list_display = ('title', 'author')
    list_filter = ('author',)
    inlines = [InlineProduct]


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(ModelAdmin):
    list_display = ('title', 'category')
    list_filter = ('category',)
    search_fields = ('title',)


admin.site.register(Product, ProductAdmin)
