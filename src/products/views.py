from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView
from django_currentuser.middleware import get_current_user
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Category, Product, ShippingAddress
from . import serializers

import requests


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


class ShippingAddressCreateView(CreateView):
    model = ShippingAddress
    fields = (
                'address_title',
                'company',
                'address_first_name',
                'address_last_name',
                'address',
                'address_2',
                'zip_code',
                'city',
                'phone',
                'entrance_code',
                'intercom',
                'stairs',
                'floor',
                'apartment_number',
                'comment',
            )

    def get_initial(self):
        user = get_current_user()
        return {
            'address_first_name': user.first_name,
            'address_last_name': user.last_name,
        }

    def get_success_url(self):
        return reverse('my-addresses')


def index(request):
    endpoint = request.build_absolute_uri('/api/categories/')
    response = requests.get(endpoint)
    categories = response.json()
    context = {
        'categories': categories,
    }
    return render(request, 'index.html', context=context)


def my_addresses(request):
    user = get_current_user()
    addresses = ShippingAddress.objects.filter(user=user)
    context = {
        'user': get_current_user(),
        'addresses': addresses,
    }
    return render(request, 'my-addresses.html', context=context)
