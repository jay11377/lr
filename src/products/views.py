from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.sites.models import Site
from django.views.generic import CreateView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Category, Product, ShippingAddress, Store
from . import serializers

import requests
import re


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

    @action(detail=False)
    def site(self, request):
        if get_current_site(request).id != 1:
            store = Store.objects.get(site_id=get_current_site(request).id)
            categories = Category.objects.filter(store=store)
            categories_json = serializers.CategorySerializer(categories, many=True)
            return Response(categories_json.data)
        else:
            return Response('')

    @action(detail=True)
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
        user = self.request.user
        return {
            'address_first_name': user.first_name,
            'address_last_name': user.last_name,
        }

    def form_valid(self, form):
        user = self.request.user
        self.object = form.save()
        # do something with self.object
        self.object.user = user
        self.object.save()
        # remember the import: from django.http import HttpResponseRedirect
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('my-addresses')


def index(request):
    if get_current_site(request).id == 1:
        return render(request, 'platform/index-platform.html')
    else:
        return render(request, 'index.html')


def my_addresses(request):
    user = request.user
    addresses = ShippingAddress.objects.filter(user=user)
    context = {
        'user': user,
        'addresses': addresses,
    }
    return render(request, 'my-addresses.html', context=context)


def category_products(request, slug):
    category = Category.objects.get(slug=slug)
    endpoint = request.build_absolute_uri('/api/categories/' + str(category.id) + '/products')
    response = requests.get(endpoint)
    products = response.json()
    context = {
        'category': category.title,
        'products': products,
    }
    return render(request, 'category.html', context=context)
