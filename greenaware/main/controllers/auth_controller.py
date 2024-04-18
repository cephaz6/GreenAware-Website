import json
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

#imports from other files
from ..models import CustomUser
from ..utils import utility as utils

User = get_user_model()

@csrf_exempt
def register_user(request):
    if request.method != 'POST':
       return redirect("")
       
    try:
        user_id = utils.generate_unique_user_id()

        data = {key: request.POST.get(key) for key in request.POST}

        email = data.get('email_address')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        user_role = "observer" if data.get('user_role') == 'on' else 'user'
        password = data.get('password')

        if not email or not first_name or not last_name or not password:
            messages.error(request, 'Missing required fields.')
            return redirect("/register")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists.')
            return redirect("/register")

        user = CustomUser.objects.create_user(email=email, user_id=user_id, first_name=first_name, last_name=last_name, user_role=user_role, password=password)
        messages.success(request, 'User registered successfully.')
        return redirect("/success-url")  # Replace "/success-url" with your desired success URL

    except json.JSONDecodeError:
        messages.error(request, 'Invalid JSON data.')
        return redirect("/register")

    except ValidationError as e:
        for field, errors in e.message_dict.items():
            for error in errors:
                messages.error(request, f'{field}: {error}')
        return redirect("/register")

    except Exception as e:
        messages.error(request, 'An error occurred. Please try again later.')
        return redirect("/register")



#Login Controller
def login_user(request):
    if request.method != 'POST':
        return redirect("")

    try:
        user_id = utils.generate_unique_user_id()

        data = {key: request.POST.get(key) for key in request.POST}

        email = data.get('email_address')
        password = data.get('password')

        print(data)

        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return redirect("/login")

        user = authenticate(request, email=email, password=password)

        if user is None:
            messages.error(request, 'Invalid email or password.')
            return redirect("/login")

        if not user.is_active:
            messages.error(request, 'Your account is not active.')
            return redirect("/login")

        if not user.is_verified:
            messages.error(request, 'Your account is not verified.')
            return redirect("/login")

        if user.user_role == 'observer':
            login(request, user)
            return redirect("/observer-dashboard")

        elif user.user_role == 'user':
            login(request, user)
            return redirect("/user-dashboard")

        else:
            messages.error(request, 'Invalid user role.')
            return redirect("/login")

    except Exception as e:
        messages.error(request, 'An error occurred. Please try again later.')
        return redirect("/login")