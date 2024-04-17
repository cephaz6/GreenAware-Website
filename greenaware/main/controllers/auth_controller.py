from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse

@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_role = request.POST.get('user_role')  # Get the user_role from the form data
            if user_role:  # If user_role is provided in the form data
                user.users.user_role = user_role  # Assign user_role to the Users model associated with the user
                user.users.save()  # Save the Users model
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('')  # Redirect to the home page after successful signup
        else:
            errors = form.errors
            return JsonResponse({'errors': errors}, status=400)  # Return form errors as JSON response
    else:
        form = UserCreationForm()
    return render(request, '', {'form': form})
