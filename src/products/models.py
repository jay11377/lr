from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe
from django.core.files.base import ContentFile
from io import BytesIO
import os
from PIL import Image
from autoslug import AutoSlugField

QUANTITY_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
)

# Create your models here.


class Store(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('title'))
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='store',
        verbose_name=_('owner'),
    )

    class Meta:
        verbose_name = _('store')
        verbose_name_plural = _('stores')

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('title'))
    slug = AutoSlugField(
        populate_from='title',
        unique=True,
        always_update=True,
    )
    author = models.ForeignKey(
        get_user_model(),
        default=1,
        on_delete=models.CASCADE,
        verbose_name=_('author'),
        editable=False,
    )
    store = models.ForeignKey(
        Store,
        default=1,
        on_delete=models.CASCADE,
        related_name='store',
        verbose_name=_('store'),
    )
    include_menu = models.BooleanField(
        default=False,
        verbose_name=_('Include menus'),
        help_text=_('This category will include menus'),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('description'),
        help_text=_('This field is not mandatory, but is useful for SEO purposes'),
    )


    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('name'))
    author = models.ForeignKey(
        get_user_model(),
        default=1,
        on_delete=models.CASCADE,
        verbose_name=_('author'),
        editable=False,
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name=_('categories'),
    )
    description = models.TextField(blank=True, verbose_name=_('description'))
    photo = models.ImageField(null=True, upload_to='products', verbose_name=_('photo'))
    thumbnail = models.ImageField(null=True, upload_to='thumbs', editable=False)
    spicy = models.BooleanField(default=False, verbose_name=_('spicy'))
    vegetarian = models.BooleanField(default=False, verbose_name=_('vegetarian'))
    tax_rate = models.ForeignKey(
        'products.TaxRate',
        default=1,
        on_delete=models.CASCADE,
        related_name='store_tax_rate',
        verbose_name=_('tax rate'),
    )
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2, verbose_name=_('price'))
    price_with_taxes = models.DecimalField(default=0, max_digits=5, decimal_places=2, verbose_name=_('price including taxes'))

    class Meta:
        verbose_name = _('dish')
        verbose_name_plural = _('dishes')

    def thumbnail_tag(self):
        return mark_safe('<img src="' + settings.MEDIA_URL + '%s" />' % (self.thumbnail))
    thumbnail_tag.short_description = _('Photo')

    def save(self, *args, **kwargs):
        """
        Make and save the thumbnail for the photo here.
        """
        if not self.make_thumbnail():
            # set to a default thumbnail
            raise Exception('Could not create thumbnail - is the file type valid?')

        super(Product, self).save(*args, **kwargs)

    def make_thumbnail(self):
        """
        Create and save the thumbnail for the photo (simple resize with PIL).
        """
        image = Image.open(self.photo)
        image.thumbnail(settings.THUMB_SIZE, Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.photo.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True

    def __str__(self):
        return self.title


class MenuOption(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name=_('title'),
        help_text=_('Title visible by the client on the website'),
    )
    author = models.ForeignKey(
        get_user_model(),
        default=1,
        on_delete=models.CASCADE,
        verbose_name=_('author'),
        editable=False,
    )
    store = models.ForeignKey(
        Store,
        default=1,
        on_delete=models.CASCADE,
        related_name='mo_store',
        verbose_name=_('store'),
    )
    admin_title = models.CharField(
        blank=True,
        max_length=200,
        verbose_name=_('Administration title'),
        help_text=_('This title is only visible by the administrator, so that he can tell apart options that could have the same name on the website. E.g: "Desert for $15 menu" and "Desert for $25 menu"'),
    )


    class Meta:
        verbose_name = _('menu option')
        verbose_name_plural = _('menu options')

    def __str__(self):
        return self.title


class MenuOptionProduct(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        default=1,
        on_delete=models.CASCADE,
        verbose_name=_('author'),
        editable=False,
    )
    store = models.ForeignKey(
        Store,
        default=1,
        on_delete=models.CASCADE,
        related_name='mop_store',
        verbose_name=_('store'),
    )
    menu_option = models.ForeignKey(
        MenuOption,
        on_delete=models.CASCADE,
        related_name='mop_option',
        verbose_name=_('option'),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='mop_product',
        verbose_name=_('product'),
    )
    quantity = models.IntegerField(
        choices=QUANTITY_CHOICES,
        verbose_name=_('quantity'),
    )


    class Meta:
        verbose_name = _('option product')
        verbose_name_plural = _('option products')

    def __str__(self):
        return self.product.title


class Menu(Product):
    options = models.ManyToManyField(
        MenuOption,
        verbose_name=_('options'),
    )


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

    class Meta:
        verbose_name = _('Tax rate')
        verbose_name_plural = _('Tax rates')

    def __str__(self):
        return "%s (%s %%)" % (self.name, self.tax_rate)


class DeliveryArea(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('name'))
    author = models.ForeignKey(
        get_user_model(),
        default=1,
        on_delete=models.CASCADE,
        verbose_name=_('author'),
        editable=False,
    )
    store = models.ForeignKey(
        Store,
        default=1,
        on_delete=models.CASCADE,
        related_name='da_store',
        verbose_name=_('store'),
    )
    minimum = models.DecimalField(
        default=0,
        max_digits=5,
        decimal_places=2,
        verbose_name=_('minimum'),
    )
    delivery_duration = models.DurationField(
        verbose_name=_('delivery duration'),
    )

    class Meta:
        verbose_name = _('delivery area')
        verbose_name_plural = _('delivery areas')

    def __str__(self):
        return self.name


class DeliveryCity(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('name'))
    author = models.ForeignKey(
        get_user_model(),
        default=1,
        on_delete=models.CASCADE,
        verbose_name=_('author'),
        editable=False,
    )
    store = models.ForeignKey(
        Store,
        default=1,
        on_delete=models.CASCADE,
        related_name='dc_store',
        verbose_name=_('store'),
    )
    delivery_area = models.ForeignKey(
        DeliveryArea,
        on_delete=models.CASCADE,
        related_name='dc_area',
        verbose_name=_('delivery area'),
    )
    zip_code = models.IntegerField(
        verbose_name=_('zip code'),
    )

    class Meta:
        verbose_name = _('delivery city')
        verbose_name_plural = _('delivery cities')

    def __str__(self):
        return self.name


class ShippingAddress(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        default=1,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        editable=False,
    )
    address_title = models.CharField(
        max_length=200,
        verbose_name=_('address title'),
        help_text=_('(Home, Office)'),
    )
    company = models.CharField(max_length=200, blank=True, verbose_name=_('company'))
    address_first_name = models.CharField(max_length=200, verbose_name=_('first name'))
    address_last_name = models.CharField(max_length=200, verbose_name=_('last name'))
    address = models.CharField(max_length=200, verbose_name=_('address'))
    address_2 = models.CharField(max_length=200, blank=True, verbose_name=_('address (2)'))
    zip_code = models.CharField(max_length=200, verbose_name=_('zip code'))
    city = models.CharField(max_length=200, verbose_name=_('city'))
    phone = models.CharField(max_length=200, verbose_name=_('phone'))
    entrance_code = models.CharField(max_length=200, blank=True, verbose_name=_('entrance code'))
    intercom = models.CharField(max_length=200, blank=True, verbose_name=_('intercom'))
    stairs = models.CharField(max_length=200, blank=True, verbose_name=_('stairs'))
    floor = models.CharField(max_length=200, blank=True, verbose_name=_('floor'))
    apartment_number = models.CharField(max_length=200, blank=True, verbose_name=_('apartment number'))
    comment = models.CharField(max_length=200, blank=True, verbose_name=_('comment'))

    class Meta:
        verbose_name = _('shipping address')
        verbose_name_plural = _('shipping addresses')

    def __str__(self):
        return self.address_title


