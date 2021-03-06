from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem
from django.utils.translation import ugettext_lazy as _


class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'
    menu = (
        ParentItem(_('Users'), children=[
            ChildItem(model='auth.user'),
            ChildItem(_('User groups'), 'auth.group'),
            ChildItem(model='products.shippingaddress'),
        ], align_right=True, icon='fa fa-users'),
        ParentItem(_('Products'), children=[
            ChildItem(model='products.category'),
            ChildItem(model='products.product'),
            ChildItem(model='products.menu'),
            # ChildItem(model='products.menuoption'),
            # ChildItem(model='products.menuoptionproduct'),
            ChildItem(_('Menu options'), 'products.menuoptionproduct'),
        ]),
        ParentItem(_('Delivery areas'), children=[
            ChildItem(_('Manage areas'), 'products.deliveryarea'),
            ChildItem(_('Manage cities'), 'products.deliverycity'),
        ]),
        ParentItem(_('Store'), children=[
            ChildItem(model='sites.site'),
            ChildItem(model='products.store'),
            ChildItem(_('Tax rates'), 'products.taxrate'),
        ]),
    )

    def ready(self):
        super(SuitConfig, self).ready()

