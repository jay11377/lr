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
        if not request.user.is_superuser:
            return qs.filter(author=request.user)
        else:
            return qs



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
    inlines = [InlineProduct]

    def changelist_view(self, request, extra_context=None):
        if not request.user.is_superuser:
            self.list_display = ('title',)
        return super(CategoryAdmin, self).changelist_view(request, extra_context)

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['author']
        else:
            return []


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(ModelAdmin):
    list_display = ('title', 'category')
    list_filter = ('category',)
    search_fields = ('title',)


admin.site.register(Product, ProductAdmin)
