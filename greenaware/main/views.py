import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


#import from other files
from main.controllers.auth_controller import *
from main.utils.authentication import get_user_dashboard_data
from main.utils.utility import fetch_weather_notes


#Define the SiteInformation File
with open('main/data/siteInformation.json') as json_file:
    site_info = json.load(json_file)

# Create your views here.
def index_page(request):
    return render(request, "index.html", {'site_info': site_info})

def contact_page(request):
    return render(request, "contact-us.html", {'site_info': site_info})



#Authentication
def register_page(request):
    return render(request, "authentication/register.html", {'site_info': site_info})

def login_page(request):
    return render(request, "authentication/login.html", {'site_info': site_info})

def logout_user(request):
    logout(request)
    return redirect("/login")


#----------- OTHER PAGES
def about(request):
    return render(request, "company/about-us.html", {'site_info': site_info})

def privacy_policy(request):
    return render(request, "company/privacy-policy.html", {'site_info': site_info})

def terms(request):
    return render(request, "company/terms-and-conditions.html", {'site_info': site_info})

def marketplace(request):
    return render(request, "api/marketplace.html", {'site_info': site_info})

def api_guide(request):
    return render(request, "api/guide.html", {'site_info': site_info})

def pricing(request):
    return render(request, "api/pricing.html", {'site_info': site_info})



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


#User Dashboard
@csrf_exempt
@login_required
def user_dashboard(request):
    return render(request, 'dashboard/user.html', {'site_info': site_info})

@login_required
def user_subscribe(request):
    return render(request, 'dashboard/pricing.html', {'site_info': site_info})

@csrf_exempt
@login_required
def user_checkout(request):
    plan = request.GET.get('plan')
    return render(request, 'dashboard/checkout.html', {'site_info': site_info})

@login_required
def user_history(request):
    return render(request, 'dashboard/payment-history.html', {'site_info': site_info})



#Observer Views
@csrf_exempt
@login_required
def add_observation(request):
    weather_notes = fetch_weather_notes()
    
    if weather_notes is not None:
        return render(request, 'dashboard/observer/add-observation.html', {'site_info': site_info, 'weather_notes': weather_notes})
    else:
        return HttpResponse('Error fetching weather notes')

@csrf_exempt
@login_required
def observations(request):
    return render(request, 'dashboard/observer/observations.html', {'site_info': site_info})


#ERROR HANDLING ROUTE 
def custom_404_view(request, exception):    
    return render(request, '404.html', {'site_info': site_info}, status=404)