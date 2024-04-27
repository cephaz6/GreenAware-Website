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
# def update_api_observer(data, user_id):
#     try:

#         # Define the URL of the remote Flask API endpoint for observer registration
#         api_url = f"http://127.0.0.1:5000/update-observer/{user_id}"

#         # Send a POST request to the API endpoint
#         response = requests.post(api_url, json=data)

#         # Check the response from the Flask API
#         if response.status_code == 200:
#             return JsonResponse({'message': '"Observer information updated successfully in the API"'}, status=200)
#         else:
#             return JsonResponse({'error': 'Failed to update observer information in the API'}, status=500)

#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)


#GRAB WEATHER CONDITIONS FROM API DB
def fetch_weather_notes():
    response = requests.get('http://127.0.0.1:5000/weather-notes')
    if response.status_code == 200:
        return response.json()
    else:
        return None

