from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Category, Product, Store


def get_user_store(user):
    return Store.objects.get(owner=user)


def get_store_categories(user):
    store = get_user_store(user)
    return Category.objects.filter(store=store)


def get_store_categories_ids(user):
    store = get_user_store(user)
    qs = Category.objects.filter(store=store).values_list('id', flat=True)
    categories_ids = list(qs)
    return categories_ids


# Filter for categories
class FilterUserAdmin(ModelAdmin):
    # Force current user as author
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        if not request.user.is_superuser:
            obj.store = get_user_store(request.user)
        obj.save()

    # Filter view with author's store
    def get_queryset(self, request):
        qs = super(FilterUserAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(store=get_user_store(request.user))
        else:
            return qs


# Flter for products
class FilterUserProductsAdmin(ModelAdmin):
    # Force current user as author
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

    # Filter view with author's store's categories' products
    def get_queryset(self, request):
        qs = super(FilterUserProductsAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(category__in=get_store_categories_ids(request.user))
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
    inlines = [InlineProduct]

    def changelist_view(self, request, extra_context=None):
        if not request.user.is_superuser:
            self.list_display = ('title',)
        else:
            self.list_display = ('title', 'author', 'store')
        return super(CategoryAdmin, self).changelist_view(request, extra_context)

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['author']
        else:
            return []

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['title', 'store']
        else:
            return ['title']


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(FilterUserProductsAdmin):
    list_filter = ('category',)
    search_fields = ('title',)

    def changelist_view(self, request, extra_context=None):
        if not request.user.is_superuser:
            self.list_display = ('title', 'category')
        else:
            self.list_display = ('title', 'category', 'author')
        return super(ProductAdmin, self).changelist_view(request, extra_context)

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['category']
        else:
            return ['category']


admin.site.register(Product, ProductAdmin)
