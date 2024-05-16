import random, string, requests, secrets
from ..models import CustomUser, ApiKey
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model, login
from django.contrib import messages
from django.shortcuts import render, redirect

User = get_user_model()

#Unique UserID Generator
def generate_unique_user_id(length=10):
    characters = string.ascii_letters + string.digits
    user_id = ''.join(random.choice(characters) for _ in range(length))

    # Check if the generated user_id already exists in the CustomUser table
    while CustomUser.objects.filter(user_id=user_id).exists():
        # If it exists, generate a new one until a unique user_id is found
        user_id = ''.join(random.choice(characters) for _ in range(length))

    return user_id.lower()


#Parsing Observer Information to API Database
def register_api_observer(data, user_id):
    try:
        data['user_id'] = user_id

        # Define the URL of the remote Flask API endpoint for observer registration
        api_url = "http://127.0.0.1:5000/signup"

        # Send a POST request to the API endpoint
        response = requests.post(api_url, json=data)

        # Check the response from the Flask API
        if response.status_code == 200:
            return JsonResponse({'message': 'Observer registration successful.'}, status=200)
        else:
            return JsonResponse({'error': 'Observer registration failed.'}, status=500)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


#Updating Observer Information in API Database
def update_api_password(user_id, new_password):
    try:
        # Fetch user information from your database or wherever it is stored
        user_info = {
            'user_id': user_id,
            'new_password': new_password
        }

        # API endpoint for updating user password
        api_url = "http://127.0.0.1:5000/update-password"

        # Send a POST request to the API endpoint with user information
        response = requests.post(api_url, json=user_info)

        # Check the response status code to ensure the operation was successful
        if response.status_code == 200:
            print("Password updated successfully in the API")
        else:
            print("Failed to update password in the API")

    except Exception as e:
        print("An error occurred while updating password in the API:", e)



#GRAB WEATHER CONDITIONS FROM API DB
def fetch_weather_notes():
    response = requests.get('http://127.0.0.1:5000/weather-notes')
    if response.status_code == 200:
        return response.json()
    else:
        return None


#GRAB ALL API KEYS FROM DB
def fetch_all_api_keys(request):
    try:
        # Fetch all active API keys from the database
        api_keys = ApiKey.objects.filter(is_active=1)
        
        # Prepare the data in JSON format
        api_keys_data = [
            {
                'user_id': api_key.user_id,
                'api_key': api_key.api_key,
                'calls': api_key.calls,
                'quota_allotted': api_key.quota_allotted
            }
            for api_key in api_keys
        ]
        
        # Return the JSON response
        return JsonResponse({'api_keys': api_keys_data}, status=200)
    
    except Exception as e:
        # Handle exceptions
        return JsonResponse({'error': str(e)}, status=500)


#REGISTER OR LOG EVERY API CALL - (API CALL LISTENER)
def register_api_call(request):
    try:
        # Extract API key and user ID from the request
        api_key = request.POST.get('api_key')
        user_id = request.POST.get('user_id')
        print(api_key, user_id)

        # Query the APIKey table for the specified API key and user ID
        api_key_obj = ApiKey.objects.filter(api_key=api_key, user=user_id).first()

        if api_key_obj:
            # Increment the call count by 1
            api_key_obj.calls += 1
            api_key_obj.save()

            return JsonResponse({'success': True, 'message': 'API call registered successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid API key or user ID.'}, status=400)

    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'}, status=500)

#VERIFY EMAIL
def activate_account(user, email):
    try:
        # Generate a random verification token
        token = secrets.token_urlsafe(32).islower()

        # Save the token to the user's record
        user.email_verification_token = token
        user.save()

        # Generate verification link with token
        verification_link = f"http://127.0.0.1:8000/verify/{token}/"

        # Render email template
        email_subject = "Verify Your Account"
        email_html_message = render_to_string('mail/activation_email.html', {'verification_link': verification_link, 'user': user})
        email_plaintext_message = strip_tags(email_html_message)

        # Send the email
        msg = EmailMultiAlternatives(
            email_subject,
            email_plaintext_message,
            'webstore.perfume@gmail.com',
            [email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()
    except Exception as e:
        # Handle exceptions
        print(f"An error occurred: {e}")


def verify_email(request, token):
    try:
        # Find the user with the provided token
        user = User.objects.get(email_verification_token=token)
    except User.DoesNotExist:
        # Handle the case where the user with the provided token doesn't exist
        messages.error(request, "Invalid verification token.")
        return redirect('/login')

    try:
        # Mark the user's email as verified
        user.is_verified = True
        user.save()

        # Log in the user
        login(request, user)

        # Redirect to a success page or display a success message
        messages.success(request, "Your email has been successfully verified.")
        return redirect('/dashboard')
    except Exception as e:
        print(e)
        # Handle other exceptions, such as database errors
        messages.error(request, f"An error occurred: {e}")
        return redirect('/login')