from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import(
    index,
    CategoriesViewSet,
    ProductViewSet,
)

__app_name__ = 'products'

router = SimpleRouter()
router.register('categories', CategoriesViewSet)
router.register('products', ProductViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('', index, name='index'),
]
