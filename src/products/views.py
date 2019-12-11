from django.shortcuts import render, redirect
# from django.views import View
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Category, Product, ShippingAddress

from . import serializers


# Create your views here.
class BaseViewSet (viewsets.ModelViewSet):
    permission_classes = (AllowAny,)


class CategoriesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()

    @detail_route()
    def products(self, request, pk=None):
        category = self.get_object()  # retrieve an object by pk provided
        products = Product.objects.filter(categories=category).distinct()
        products_json = serializers.ProductSerializer(products, many=True)
        return Response(products_json.data)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()


def index(request):
    context = {
        'num': 3,
    }
    return render(request, 'index.html', context=context)
