import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

import jwt

#imports from other files
from ..models import CustomUser

#Update User Information
@csrf_exempt
def update_profile(request):
    try:
        data = {key: request.POST.get(key) for key in request.POST}

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        user_id = data.get('user_id')

        # Retrieve user object
        user = CustomUser.objects.get(user_id=user_id)

        # Update user profile fields
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect("/update-profile")

    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred. Please try again later.')
        return redirect("/update-profile")