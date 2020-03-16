from django.urls import include, path
from django.views.generic import CreateView
from rest_framework.routers import SimpleRouter

from .views import(
    index,
    ShippingAddressCreateView,
    my_addresses,
    CategoriesViewSet,
    ProductViewSet,
    category_products,
)

__app_name__ = 'products'

router = SimpleRouter()
router.register('categories', CategoriesViewSet)
router.register('products', ProductViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('accounts/', include('allauth.urls')),
    path('', index, name='index'),
    path('accounts/add-address/', ShippingAddressCreateView.as_view(), name='add-address'),
    path('accounts/my-addresses/', my_addresses, name='my-addresses'),
    path('<slug:slug>/', category_products, name='category'),
]
