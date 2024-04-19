from main.utils.authentication import get_user_dashboard_data  # Import your function to retrieve user data

def user_data(request):
    """
    Adds user data to the context.
    """
    if request.user.is_authenticated:
        user_data = get_user_dashboard_data(request)  # Call your function to retrieve user data
        return {'user_data': user_data}  # Return user data in the context
    else:
        return {}  # Return an empty context if user is not authenticated
