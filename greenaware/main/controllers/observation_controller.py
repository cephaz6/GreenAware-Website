import random, string, requests
from ..models import CustomUser
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError


#Parsing New Observation Information to API Database
def add_new_observation(request, jwt_token):
    try:
        # jwt_token = request.session.get('access_token')

        headers = {
            'Authorization': f'Bearer {jwt_token}'
        }

        #Remote Flask API endpoint to add Observation
        api_url = "http://127.0.0.1:5000/add-observation"

        # Send a POST request to the API endpoint
        response = requests.post(api_url, json=request, headers=headers)

        # Check the response from the Flask API
        if response.status_code == 200:
            return JsonResponse({'message': 'Observation Added Successfully'}, status=200)
        else:
            print(request)
            return JsonResponse({'error': 'Observation failed.'}, status=500)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)