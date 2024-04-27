import random, string, requests
from ..models import CustomUser
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError


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

