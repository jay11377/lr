from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe
from django.core.files.base import ContentFile
from io import BytesIO
import os
from PIL import Image

# Create your models here.


class Store(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('title'))
    domain = models.CharField(max_length=200, verbose_name=_('domain'))
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
        related_name=_('store'),
        verbose_name=_('store'),
    )


    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.title


class Product(models.Model):
    categories = models.ManyToManyField(
        Category,
        verbose_name=_('categories'),
    )
    author = models.ForeignKey(
        get_user_model(),
        default=1,
        on_delete=models.CASCADE,
        verbose_name=_('author'),
        editable=False,
    )
    title = models.CharField(max_length=200, verbose_name=_('name'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2, verbose_name=_('price'))
    photo = models.ImageField(null=True, upload_to='products', verbose_name=_('photo'))
    thumbnail = models.ImageField(null=True, upload_to='thumbs', editable=False)
    spicy = models.BooleanField(default=False, verbose_name=_('spicy'))
    vegetarian = models.BooleanField(default=False, verbose_name=_('vegetarian'))

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
