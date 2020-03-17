from django.contrib.sites.shortcuts import get_current_site
from .models import Store
import requests


def global_variables(request):
    store_title = Store.objects.get(site_id=get_current_site(request).id).title

    if get_current_site(request).id == 1:
        return {'store_title': None, 'categories': None}
    else:
        endpoint = request.build_absolute_uri('/api/categories/site/')
        response = requests.get(endpoint)
        categories = response.json()
        return {'store_title': store_title, 'categories': categories}
