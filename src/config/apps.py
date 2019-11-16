from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem


class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'
    menu = (
        ParentItem('Users', children=[
            ChildItem(model='auth.user'),
            ChildItem('User groups', 'auth.group'),
        ], align_right=True, icon='fa fa-users'),
        ParentItem('Products', children=[
            ChildItem(model='products.category'),
            ChildItem(model='products.product'),
        ]),
        ParentItem('Store', children=[
            ChildItem(model='products.store'),
            ChildItem(model='products.taxrate'),
        ]),
    )


    def ready(self):
        super(SuitConfig, self).ready()

