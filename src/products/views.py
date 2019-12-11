from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Category, Product, ShippingAddress
from .forms import CreateAccountForm

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


class CreateAccountView(View):
    def get(self, *args, **kwargs):
        # form
        form = CreateAccountForm()
        context = {
            'form': form,
        }
        return render(self.request, 'create-account.html', context)

    def post(self, *args, **kwargs):
        form = CreateAccountForm(self.request.POST or None)
        if form.is_valid():
            # User
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')

            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                confirm_password=confirm_password,
            )
            user.save()

            # Address
            address_title = form.cleaned_data.get('address_title')
            company = form.cleaned_data.get('company')
            address_first_name = form.cleaned_data.get('address_first_name')
            address_last_name = form.cleaned_data.get('address_last_name')
            address = form.cleaned_data.get('address')
            address_2 = form.cleaned_data.get('address_2')
            zip_code = form.cleaned_data.get('zip_code')
            city = form.cleaned_data.get('city')
            phone = form.cleaned_data.get('phone')
            entrance_code = form.cleaned_data.get('entrance_code')
            intercom = form.cleaned_data.get('intercom')
            stairs = form.cleaned_data.get('stairs')
            floor = form.cleaned_data.get('floor')
            apartment_number = form.cleaned_data.get('apartment_number')
            comment = form.cleaned_data.get('comment')

            shipping_address = ShippingAddress(
                address_title=address_title,
                company=company,
                address_first_name=address_first_name,
                address_last_name=address_last_name,
                address=address,
                address_2=address_2,
                zip_code=zip_code,
                city=city,
                phone=phone,
                entrance_code=entrance_code,
                intercom=intercom,
                stairs=stairs,
                floor=floor,
                apartment_number=apartment_number,
                comment=comment,
            )
            shipping_address.save()
            return redirect('index')


def index(request):
    context = {
        'num': 3,
    }
    return render(request, 'index.html', context=context)
