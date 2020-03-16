import requests

def categories(request):
    endpoint = request.build_absolute_uri('/api/categories/site/')
    response = requests.get(endpoint)
    categories = response.json()
    return {'categories': categories}
