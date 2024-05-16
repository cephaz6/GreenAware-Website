import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponseServerError
from django.conf import settings

#import from other files
from main.controllers.auth_controller import *
from main.controllers.user_controller import *
from main.controllers.observation_controller import *
from main.utils.authentication import get_user_dashboard_data
from main.utils.utility import *
from main.utils.custom_decorators import observer_only
from main.models import *
import stripe


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


def activate(request, token):
    return verify_email(request, token)


#User Dashboard
@login_required
def user_dashboard(request):
    return render(request, 'dashboard/user.html', {'site_info': site_info})

@login_required
def user_subscribe(request):
    return render(request, 'dashboard/pricing.html', {'site_info': site_info})

@csrf_exempt
@login_required
def user_checkout(request):
    try:
        plan = request.GET.get('plan')
        if request.method == 'GET':
            return render(request, 'dashboard/checkout.html', {'site_info': site_info, 'plan':plan})
        elif request.method == 'POST':
            return checkout(request, site_info)
    except Exception as e:
        return HttpResponseServerError("An error occurred: {}".format(str(e)))

@csrf_exempt
@login_required
def pay(request, payment_intent_id):
    try:
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        client_secret = stripe.PaymentIntent.retrieve(payment_intent_id)
        if request.method == 'GET':
            return render(request, 'dashboard/pay.html', {'site_info': site_info, 'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY})
        elif request.method == 'POST':
            return make_payment(request, client_secret)
    except Exception as e:
        return HttpResponseServerError("An error occurred: {}".format(str(e)))


@login_required
def user_services(request):
    if request.method == 'GET':
        try:
            user = request.user
            api_keys = ApiKey.objects.filter(user=user)
            if api_keys:
                return render(request, 'dashboard/my-services.html', {'site_info': site_info, 'api_keys': api_keys})
            else:
                messages.error(request, "You do not have any active API KEY, Generate One Now!!!!")
                return render(request, 'dashboard/my-services.html', {'site_info': site_info, 'api_keys': api_keys})
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('/dashboard')


@csrf_exempt
@login_required
def generate_key(request):
    return generate_api_key(request)


@login_required
def user_history(request):
    return render(request, 'dashboard/payment-history.html', {'site_info': site_info})

@csrf_exempt
@login_required
def user_update_profile(request):
    print(request.method)
    if request.method == 'GET':
        return render(request, 'dashboard/update-profile.html', {'site_info': site_info})
    elif request.method == 'POST':
        return update_profile(request)

@csrf_exempt
@login_required
def user_update_password(request):
    return update_password(request)


#Observer Views
@csrf_exempt
@login_required
@observer_only
def add_observation(request):
    if request.method == 'GET':
        weather_notes = fetch_weather_notes()
        if weather_notes is not None:
            return render(request, 'dashboard/observer/add-observation.html', {'site_info': site_info, 'weather_notes': weather_notes})
        else:
            return HttpResponse('Error fetching weather notes')
    elif request.method == 'POST':
        jwt_token = request.session.get('access_token')
        data = {key: request.POST.get(key) for key in request.POST}
        return add_new_observation(request, data, jwt_token)


#BULK OBSERVATION
@csrf_exempt
@login_required
@observer_only
def bulk_observations(request):
    try:
        print(request.method)
        if 'file' not in request.FILES:
            messages.error(request, "No File Selected")
            return redirect('/new-observation')

        json_file = request.FILES['file']
        json_data = json_file.read()

        print(json_data)

        # Send the JSON data to the Flask API
        response = requests.post(
            'http://12.0.0.1:5000/upload-bulk', 
            files={'file': ('file.json', json_data, 'application/json')}
        )

        if response.status_code == 200:
            return HttpResponse('File uploaded and processed successfully')
        else:
            return HttpResponse(f'Failed to upload file: {response.text}', status=response.status_code)
    except requests.exceptions.RequestException as e:
        messages.error(request, "An error occurred")
        return redirect('/new-observation')   

#VIEW OBSERVATIONS (OBSERVER)
@login_required
@observer_only
def observations(request):
    user = request.user.user_id
    observations = []  # Initialize with an empty list
    try:
        observations = fetch_observations(request, user)
        if observations:
            return render(request, 'dashboard/observer/observations.html', {'site_info': site_info, 'observations': observations})
    except Exception as e:
        messages.error(request, f'An error occurred: {e}')
    # Render the template even if there was an error to show any relevant error message
    return render(request, 'dashboard/observer/observations.html', {'site_info': site_info, 'observations': observations})

#EDIT OBSERVATION
@login_required
@observer_only
def edit_observation(request, observation_id):
    jwt_token = request.session.get('access_token')

    if request.method == 'GET':
        try:
            weather_notes = fetch_weather_notes()
            observation = fetch_observation(request, observation_id, jwt_token)
            if observation:
                return render(request, 'dashboard/observer/edit-observation.html', {'site_info': site_info, 'observation': observation, 'weather_notes': weather_notes})
            else:
                messages.error(request, "Error Fetching Observation Data")
                return redirect('/view-observations')
        except Exception as e:
            print(e)
            messages.error(request, f"An error occurred: {e}")
            return redirect('/view-observations')

    elif request.method == 'POST':
        try:
            print(request.method)
            update_observation(request, observation_id, jwt_token)
            messages.success(request, "Observation updated successfully")
        except Exception as e:
            messages.error(request, f"Failed to update observation: {e}")
        return redirect('/view-observations')



#SYSTEM
# @csrf_exempt
def fetch_api_keys(request):
    return fetch_all_api_keys(request)

@csrf_exempt
def register_call(request):
    return register_api_call(request)


#ERROR HANDLING ROUTE 
def custom_404_view(request, exception):    
    return render(request, '404.html', {'site_info': site_info}, status=404)

def error_401(request):
    return render(request, "401.html", {'site_info': site_info})