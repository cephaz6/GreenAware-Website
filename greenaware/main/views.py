from django.shortcuts import render
import json
from .controllers.auth_controller import *

with open('main/data/siteInformation.json') as json_file:
    site_info = json.load(json_file)

# Create your views here.
def index_page(request):
    return render(request, "index.html", {'site_info': site_info})

def contact_page(request):
    return render(request, "contact-us.html")

def register_page(request):
    return render(request, "authentication/register.html", {'site_info': site_info})

def login_page(request):
    return render(request, "authentication/login.html", {'site_info': site_info})


#Controllers
