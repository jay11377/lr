from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Category, Product, Store, TaxRate, DeliveryArea, DeliveryCity, Menu, MenuOption, MenuOptionProduct, ShippingAddress
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.forms import SelectMultiple
from django.utils.encoding import force_text


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


# Filter for products
class FilterUserProductsAdmin(ModelAdmin):
    # force CSS for multiple select fields
    formfield_overrides = {models.ManyToManyField: {'widget': SelectMultiple(attrs={'style': 'width:200px; height:80px'})}, }

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
class StoreAdmin(ModelAdmin):
    list_display = ('title', 'owner')
    search_fields = ('title',)


admin.site.register(Store, StoreAdmin)


class CategoryAdmin(FilterUserAdmin):

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display = ('title', 'author', 'store', 'include_menu', 'description')
        else:
            self.list_display = ('title', 'include_menu', 'description')
        return super(CategoryAdmin, self).changelist_view(request, extra_context)

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['author']
        else:
            return []

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['title', 'store', 'include_menu', 'description']
        else:
            return ['title', 'include_menu', 'description']


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


class MenuCategoriesListFilters(admin.SimpleListFilter):
    title = _('category')
    parameter_name = 'categories__id__exact'
    default_value = None

    def lookups(self, request, model_admin):
        categories_list = []
        if request.user.is_superuser:
            queryset = Category.objects.filter(include_menu=1)
        else:
            queryset = Category.objects.filter(store=get_user_store(request.user), include_menu=1)
        for category in queryset:
            categories_list.append((str(category.id), category.title))
        return sorted(categories_list, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(categories__id__exact=self.value())
        return queryset


class MenuOptionsListFilters(admin.SimpleListFilter):
    title = _('option')
    parameter_name = 'menu_option_id'
    default_value = None

    def lookups(self, request, model_admin):
        options_list = []
        if request.user.is_superuser:
            queryset = MenuOption.objects.all()
        else:
            queryset = MenuOption.objects.filter(store=get_user_store(request.user))
        for option in queryset:
            options_list.append((str(option.id), option.title))
        return sorted(options_list, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(menu_option_id=self.value())
        return queryset

    def value(self):
        """
        Overriding this method will allow us to always have a default value.
        """
        value = super(MenuOptionsListFilters, self).value()
        if value is None:
            if self.default_value is None:
                # If there is at least one Species, return the first by name. Otherwise, None.
                first_option = MenuOption.objects.order_by('title').first()
                value = None if first_option is None else first_option.id
                self.default_value = value
            else:
                value = self.default_value
        return str(value)

    def choices(self, changelist):
        """Copied from source code to remove the "All" Option"""
        yield {
            'selected': self.value() is None,
            'query_string': changelist.get_query_string({}, [self.parameter_name]),
            'display': '',
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == force_text(lookup),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}, []),
                'display': title,
            }


class ProductAdmin(FilterUserProductsAdmin):
    search_fields = ('title',)

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display = ('thumbnail_tag', 'title', 'price_with_taxes')
        else:
            self.list_display = ('thumbnail_tag', 'title', 'get_categories', 'price_with_taxes')
        self.list_display_links = ('title',)
        return super(ProductAdmin, self).changelist_view(request, extra_context)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'categories':
            if not request.user.is_superuser:
                kwargs["queryset"] = Category.objects.filter(store=get_user_store(request.user))
        return super(ProductAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'tax_rate':
            if not request.user.is_superuser:
                kwargs["queryset"] = TaxRate.objects.filter(store=get_user_store(request.user))
        return super(ProductAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

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


class MenuAdmin(ProductAdmin):

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'categories':
            if request.user.is_superuser:
                kwargs["queryset"] = Category.objects.filter(include_menu=1)
            else:
                kwargs["queryset"] = Category.objects.filter(store=get_user_store(request.user), include_menu=1)
        return super(ProductAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display = ('thumbnail_tag', 'title', 'get_options')
        else:
            self.list_display = ('thumbnail_tag', 'title', 'get_categories', 'get_options')
        self.list_display_links = ('title',)
        return super(ProductAdmin, self).changelist_view(request, extra_context)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'options':
            if not request.user.is_superuser:
                kwargs["queryset"] = MenuOption.objects.filter(store=get_user_store(request.user))
        return super(MenuAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def get_options(self, request):
        options_html = "".join([format_html('{}</br>', o.title) for o in request.options.all()])
        return format_html(options_html)
    get_options.short_description = _('options')

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return [MenuCategoriesListFilters]
        else:
            return [MenuCategoriesListFilters]

admin.site.register(Menu, MenuAdmin)


class MenuOptionAdmin(FilterUserAdmin):

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display = ('title', 'admin_title', 'author', 'store')
        else:
            self.list_display = ('title', 'admin_title')
        return super(MenuOptionAdmin, self).changelist_view(request, extra_context)

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['title', 'store', 'admin_title']
        else:
            return ['title', 'admin_title']


admin.site.register(MenuOption, MenuOptionAdmin)


class MenuOptionProductAdmin(FilterUserAdmin):

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display = ('product', 'quantity', 'menu_option', 'author', 'store')
        else:
            self.list_display = ('product', 'quantity')
        return super(MenuOptionProductAdmin, self).changelist_view(request, extra_context)

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['menu_option', 'product', 'store', 'quantity']
        else:
            return ['menu_option', 'product', 'quantity']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'menu_option':
            if not request.user.is_superuser:
                kwargs["queryset"] = MenuOption.objects.filter(store=get_user_store(request.user))
        return super(MenuOptionProductAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return [MenuOptionsListFilters]
        else:
            return [MenuOptionsListFilters]


admin.site.register(MenuOptionProduct, MenuOptionProductAdmin)


class TaxRateAdmin(FilterUserAdmin):
    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display = ('name', 'tax_rate', 'store')
        else:
            self.list_display = ('name', 'tax_rate')
        return super(TaxRateAdmin, self).changelist_view(request, extra_context)

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['name', 'tax_rate', 'store']
        else:
            return ['name', 'tax_rate']


admin.site.register(TaxRate, TaxRateAdmin)


class DeliveryAreaAdmin(FilterUserAdmin):
    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display = ('name', 'author', 'store', 'minimum', 'delivery_duration')
        else:
            self.list_display = ('name', 'minimum', 'delivery_duration')
        return super(DeliveryAreaAdmin, self).changelist_view(request, extra_context)

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['name', 'store', 'minimum', 'delivery_duration']
        else:
            return ['name', 'minimum', 'delivery_duration']


admin.site.register(DeliveryArea, DeliveryAreaAdmin)


class DeliveryCityAdmin(FilterUserAdmin):
    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display = ('name', 'author', 'store', 'delivery_area', 'zip_code')
        else:
            self.list_display = ('name', 'delivery_area', 'zip_code')
        return super(DeliveryCityAdmin, self).changelist_view(request, extra_context)

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['name', 'store', 'delivery_area', 'zip_code']
        else:
            return ['name', 'delivery_area', 'zip_code']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'delivery_area':
            if not request.user.is_superuser:
                kwargs["queryset"] = DeliveryArea.objects.filter(store=get_user_store(request.user))
        return super(DeliveryCityAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(DeliveryCity, DeliveryCityAdmin)


class ShippingAddressAdmin(FilterUserAdmin):
    title = _('shipping addresses')
    # def changelist_view(self, request, extra_context=None):
    #     if request.user.is_superuser:
    #         self.list_display = ('name', 'author', 'store', 'delivery_area', 'zip_code')
    #     else:
    #         self.list_display = ('name', 'delivery_area', 'zip_code')
    #     return super(DeliveryCityAdmin, self).changelist_view(request, extra_context)

    # def get_fields(self, request, obj=None):
    #     if request.user.is_superuser:
    #         return ['name', 'store', 'delivery_area', 'zip_code']
    #     else:
    #         return ['name', 'delivery_area', 'zip_code']

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'delivery_area':
    #         if not request.user.is_superuser:
    #             kwargs["queryset"] = DeliveryArea.objects.filter(store=get_user_store(request.user))
    #     return super(DeliveryCityAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(ShippingAddress, ShippingAddressAdmin)
