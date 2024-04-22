import requests
from ..models import CustomUser
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError


#Parsing New Observation Information to API Database
def add_new_observation(request, data, jwt_token):

    try:
        # data = {key: data.POST.get(key) for key in data.POST}
        print(data)
        print(jwt_token)
        
        headers = {'Authorization': f'Bearer {jwt_token}'}
        api_url = "http://127.0.0.1:5000/add-observation"
        response = requests.post(api_url, json=data, headers=headers)

        if response.status_code == 200 or response.status_code == 201:
            # return JsonResponse({'message': 'Observation Added Successfully'}, status=200)
            messages.success(request, 'Observation Added Successfully')
            return redirect("/view-observations")
        else:
            messages.error(request, 'Observation Failed')
            return redirect("/new-observation")
            # return JsonResponse({'error': response.json()}, status=500)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


#GRAB OBSERVER'S OBSERVATIOINS FROM API DB
def fetch_observations(request):
    try:
        # URL of the Flask app endpoint that provides observation data
        api_url = "http://127.0.0.1:5000/get-observations"

        # JWT token obtained from Django session
        jwt_token = request.session.get('access_token')

        # Headers with JWT token for authorization
        headers = {'Authorization': f'Bearer {jwt_token}'}

        # Make a GET request to the Flask API endpoint with JWT token in headers
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            # Parse the JSON response containing observations
            return response.json()
        else:
            return JsonResponse({'error': 'Failed to fetch observations'}, status=response.status_code)

    except requests.RequestException as e:
        # Handle request errors 
        print(e)
        return None