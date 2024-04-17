from django.shortcuts import render
from django.http import HttpResponse
import json
from .controllers.auth_controller import *

# Create your views here.
def index_page(request):
    with open('main/siteInformation.json') as json_file:
        site_info = json.load(json_file)
    return render(request, "index.html", {'site_info': site_info})

def contact_page(request):
    return render(request, "contact-us.html")

def register(request):
    return signup(request)

# def custom_404(request, exception=None):
#     return render(request, '404.html', status=404)