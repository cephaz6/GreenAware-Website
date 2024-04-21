from django.shortcuts import redirect

def observer_only(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            if not request.user.is_authenticated:
                return redirect('/login')  # Redirect to login page if user is not authenticated
            elif request.user.user_role not in ['observer', 'admin']:
                return redirect('/unauthorized')  # Redirect to unauthorized page if user role is not 'observer' or 'admin'
            return view_func(request, *args, **kwargs)
        except Exception as e:
            print(f"An error occurred in the observer_only decorator: {e}")
            return redirect('error')  # Redirect to error page if an exception occurs
    return wrapper