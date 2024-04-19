import json
from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse



from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.exceptions import ImproperlyConfigured


import jwt
from django.conf import settings
from datetime import datetime, timedelta

#imports from other files
from ..models import CustomUser
from main.utils import  utility as utils
# from main.utils import activate_account

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

        # Validate email address
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email address.')
            return redirect("/register")

        if not first_name or not last_name or not password:
            messages.error(request, 'Missing required fields.')
            return redirect("/register")

        # Validate password strength
        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, f'{", ".join(e)}')
            return redirect("/register")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists.')
            return redirect("/register")

        if user_role == "observer":
            utils.register_api_observer(data, user_id)

        user = CustomUser.objects.create_user(email=email, user_id=user_id, first_name=first_name, last_name=last_name, user_role=user_role, password=password)
        # Send activation email
        activate_account(user, email)

        messages.success(request, 'User registered successfully.')
        return redirect("/success-url")

    except json.JSONDecodeError:
        messages.error(request, 'Invalid JSON data.')
        return redirect("/register")

    except ValidationError as e:
        for field, errors in e.message_dict.items():
            for error in errors:
                messages.error(request, f'{field}: {error}')
        return redirect("/register")

    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred. Please try again later.')
        return redirect("/register")


#Activate User
def activate_account(user, email):
    try:
        # Generate a unique activation token
        activation_token = default_token_generator.make_token(user)

        # Build the activation link
        activation_link = reverse('activate', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': activation_token})

        # Send activation email
        subject = 'Activate Your Account'
        message = render_to_string('mail/activation_email.html', {'activation_link': activation_link})
        send_mail(subject, message, 'cephasblog@gmail.com', [email])

    except Exception as e:
        # Handle any exceptions that might occur
        raise ImproperlyConfigured(f"Activation email could not be sent: {e}")





#Login Controller
@csrf_exempt
def login_user(request):
    if request.method != 'POST':
        return redirect("")

    try:
        data = {key: request.POST.get(key) for key in request.POST}

        email = data.get('email_address')
        password = data.get('password')

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

        # Generate JWT token
        token_payload = {
            'user_id': user.user_id,
            'exp': datetime.utcnow() + timedelta(days=1)  # Token expiration time
        }
        jwt_token = jwt.encode(token_payload, settings.JWT_KEY, algorithm='HS256')

        # Set JWT token in session or response cookies
        request.session['access_token'] = jwt_token
        print(jwt_token)

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
        print(e)
        messages.error(request, 'An error occurred. Please try again later.')
        return redirect("/login")