from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class RedirectIfAuthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of URLs that should redirect to 'home' if user is authenticated
        restricted_urls = [
            reverse('signup'),
            reverse('signup_otp'),
            reverse('signin')
            # Add more URLs here if needed
        ]

        if request.user.is_authenticated and request.path in restricted_urls:
            messages.warning(request, "You are already logged in.")
            return redirect('home')  # Redirect back to the current path
        else:
            response = self.get_response(request)

        # Add headers to prevent caching
        if response.status_code == 200:
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'

        return response
    
class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of URLs that should redirect to 'signin' if user is not authenticated
        restricted_urls = [
            reverse('profile'),
            reverse('cart'),
            reverse('add_to_cart'),
            # reverse('remove_from_cart'),
            reverse('wishlist'),
            reverse('add_to_wishlist'),
            
            reverse('order'),
            
            reverse('address'),
            
            # Add more URLs here if needed
        ]

        if not request.user.is_authenticated and request.path in restricted_urls:
            messages.warning(request, 'Please login to access this page.')  # Message for unauthenticated users
            return redirect('signin')  # Redirect to 'signin' if not authenticated

        response = self.get_response(request)

        # Add headers to prevent caching for restricted pages
        if response.status_code == 200 and request.path in restricted_urls:
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'

        return response 
    
class LogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path == reverse('logout'):
            messages.warning(request, "You are already logged out.")
            return redirect('home')

        response = self.get_response(request)
            
        return response