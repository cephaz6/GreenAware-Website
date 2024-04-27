import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from main.utils.utility import *
from django.contrib.auth.hashers import make_password

from django.conf import settings
import jwt
import stripe

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


#Payment Checkout
@csrf_exempt
def checkout(request, site_info):
    try:
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        plan = request.POST.get('plan')
        price = 50 if plan == 'professional' else 100
        
        # Create a PaymentIntent with the correct amount
        intent = stripe.PaymentIntent.create(
            amount=price,
            currency='gbp',
            description='Product Purchase',
        )
        
        if plan == 'professional':
            payment_url = "https://buy.stripe.com/test_00g0391wP2Hc4Ew001?payment_intent={}".format(intent.client_secret)
        else:
            payment_url = "https://buy.stripe.com/test_8wMg27grJchM8UMbIK?payment_intent={}".format(intent.client_secret)

        # Redirect the user to the Stripe payment page
        return redirect(payment_url)
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})
        
# @csrf_exempt
# def checkout(request, site_info):
#     try:
#         stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
#         data = {key: request.POST.get(key) for key in request.POST}
#         if request.method == 'POST':
#             # Process form data
#             print(data)
            
#             first_name = data.get('first_name', '')
#             last_name = data.get('last_name', '')
#             plan = data.get('plan')
#             name = first_name + last_name
#             phone = data.get('phone')
#             price = 120 if plan == 'professional' else 500

#             address = data.get('address')
#             country = data.get('country')

#             # Create Stripe PaymentIntent
#             intent = stripe.PaymentIntent.create(
#                 amount=price,  # Amount in cents
#                 currency='usd',
#                 description='Product Purchase',
#             )
#             print(plan)
#             print(intent)
#             # Redirect to pay view with PaymentIntent ID
#             return redirect('pay', payment_intent_id=intent.id)

#         return render(request, f'checkout.html?plan={plan}', {'site_info':site_info, 'plan': plan})
#     except Exception as e:
#         print(e)
#         messages.error(request, 'An error occurred. Please try again later.')
#         return redirect(f"/checkout?plan={plan}", {'site_info':site_info, 'plan': plan})

#Finalize Payment
def make_payment(request, client_secret):
    if request.method == 'POST':
        try:
            intent = stripe.PaymentIntent.retrieve(client_secret)
            # Update database with payment information
            # Update transaction history table
            messages.success(request, 'Payment successful!')
            return redirect('payment-success')
        except stripe.error.CardError as e:
            # Display error message to user
            messages.error(request, f'Error: {e.error.message}')
            return redirect('checkout')

    return render(request, 'pay.html', {'client_secret': client_secret, 'name': request.POST['name']})
