from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem
from django.utils.translation import ugettext_lazy as _


class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'
    menu = (
        ParentItem(_('Users'), children=[
            ChildItem(model='auth.user'),
            ChildItem(_('User groups'), 'auth.group'),
        ], align_right=True, icon='fa fa-users'),
        ParentItem(_('Products'), children=[
            ChildItem(model='products.category'),
            ChildItem(model='products.product'),
        ]),
        ParentItem(_('Store'), children=[
            ChildItem(model='products.store'),
            ChildItem(_('Tax rates'), 'products.taxrate'),
        ]),
    )


    def ready(self):
        super(SuitConfig, self).ready()

