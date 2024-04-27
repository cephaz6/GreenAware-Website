import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from main.utils.utility import *
from django.contrib.auth.hashers import make_password

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

#Password Update
@csrf_exempt
def update_password(request):
    if request.method == 'POST':
        # Check if the hidden _method field is present and set to PUT
        if request.POST.get('_method') == 'PUT':
            # Change the request method to PUT
            request.method = 'PUT'

        try:
            user_id = request.POST.get('user_id')
            new_password = request.POST.get('new_password')
            retype_new_password = request.POST.get('retype_new_password')

            # Input validation
            if not new_password or not retype_new_password:
                messages.error(request, 'Please enter a new password.')
                return redirect('/update-password')

            # Password match check
            if new_password != retype_new_password:
                messages.error(request, 'Passwords do not match.')
                return redirect('/update-password')

            # Retrieve user object
            user = CustomUser.objects.get(user_id=user_id)

            # Update user password
            user.set_password(new_password)
            user.save()

            # Update password in the API if user role is "observer"
            if user.user_role == "observer":
                update_api_password(user_id, new_password)

            messages.success(request, 'Password updated successfully.')
            return redirect('/update-password')

        except CustomUser.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('/update-password')

        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return redirect('/update-password')

        except ValueError as e:
            messages.error(request, f'An error occurred: {e}')
            return redirect('/update-password')