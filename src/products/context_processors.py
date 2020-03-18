from django.contrib.sites.shortcuts import get_current_site
from .models import Store
import requests


def global_variables(request):
    if get_current_site(request).id == 1:
        return {'store': None, 'categories': None}
    else:
        store = Store.objects.get(site_id=get_current_site(request).id).title
        endpoint = request.build_absolute_uri('/api/categories/site/')
        response = requests.get(endpoint)
        categories = response.json()
        return {'store': store, 'categories': categories}
