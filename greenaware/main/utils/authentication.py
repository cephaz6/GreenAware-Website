from django.http import HttpResponseServerError

def get_user_dashboard_data(request):
    try:
        # Retrieve the currently logged-in user
        user = request.user
        
        return user
    except Exception as e:
        # Log the error for debugging purposes
        print(f"An error occurred while retrieving user data: {e}")
        # Return an error response if an exception occurs
        return HttpResponseServerError('Internal Server Error')
