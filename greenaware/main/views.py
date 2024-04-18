import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

#import from other files
from main.controllers.auth_controller import *


#Define the SiteInformation File
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


#----------- OTHER PAGES
def about(request):
    return render(request, "company/about-us.html", {'site_info': site_info})

def privacy_policy(request):
    return render(request, "company/privacy-policy.html", {'site_info': site_info})

def terms(request):
    return render(request, "company/terms-and-conditions.html", {'site_info': site_info})



#Controllers
@csrf_exempt
def register(request):
    return register_user(request)

@csrf_exempt
def login(request):
    return login_user(request)

@csrf_exempt
def activate(request):
    return activate_account(request)



#ERROR HANDLING ROUTE 
# def custom_404(request, exception):
#     return render(request, "404.html", status=404)