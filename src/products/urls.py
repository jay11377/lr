from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

__app_name__ = 'products'

router = SimpleRouter()
router.register('categories', views.CategoriesViewSet)
router.register('products', views.ProductViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]
