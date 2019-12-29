from django.shortcuts import render
from django.urls import reverse
from django.contrib.sites.models import Site
from django.views.generic import CreateView
from django_currentuser.middleware import get_current_user
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Category, Product, ShippingAddress, Store
from . import serializers

import requests
import re


def get_site_id(host):
    domain = get_domain(host)
    site = Site.objects.get(domain=domain)
    return site.id


def get_domain(host):
    replace = {
        ":8000": "",
    }
    pattern = "|".join(map(re.escape, replace.keys()))
    return re.sub(pattern, lambda m: replace[m.group()], host)

# Create your views here.


class BaseViewSet (viewsets.ModelViewSet):
    permission_classes = (AllowAny,)


class CategoriesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()

    @list_route()
    def site(self, request):
        url_home = request.get_host()
        site_id = get_site_id(url_home)
        store = Store.objects.get(site_id=site_id)
        categories = Category.objects.filter(store=store)
        categories_json = serializers.CategorySerializer(categories, many=True)
        return Response(categories_json.data)

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
    endpoint = request.build_absolute_uri('/api/categories/site/')
    response = requests.get(endpoint)
    categories = response.json()

    url_home = request.get_host()
    site_id = get_site_id(url_home)
    store = Store.objects.get(site_id=site_id)
    context = {
        'store': store.title,
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
