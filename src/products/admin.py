from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Category, Product, Store
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _


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
            return qs.filter(categories__in=get_store_categories_ids(request.user))
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


class CategoriesListFilters(admin.SimpleListFilter):
    title = _('category')
    parameter_name = 'categories__id__exact'
    default_value = None

    def lookups(self, request, model_admin):
        categories_list = []
        if request.user.is_superuser:
            queryset = Category.objects.all()
        else:
            queryset = Category.objects.filter(store=get_user_store(request.user))
        for category in queryset:
            categories_list.append((str(category.id), category.title))
        return sorted(categories_list, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(categories__id__exact=self.value())
        return queryset


class ProductAdmin(FilterUserProductsAdmin):
    search_fields = ('title',)

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display = ('thumbnail_tag', 'title', 'category', 'get_categories', 'author')
        else:
            self.list_display = ('thumbnail_tag', 'title', 'category', 'get_categories')
        self.list_display_links = ('title',)
        return super(ProductAdmin, self).changelist_view(request, extra_context)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'categories':
            if not request.user.is_superuser:
                kwargs["queryset"] = Category.objects.filter(store=get_user_store(request.user))
        return super(ProductAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return [CategoriesListFilters]
        else:
            return [CategoriesListFilters]

    def get_categories(self, request):
        categories_html = "".join([format_html('{}</br>', c.title) for c in request.categories.all()])
        return format_html(categories_html)
    get_categories.short_description = _('categories')


admin.site.register(Product, ProductAdmin)
