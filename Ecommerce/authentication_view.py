import random
import string
from django.contrib.auth.models import User, auth
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from .tasks import send_signup_email
from django.core.mail import EmailMessage


def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').capitalize()
        last_name = request.POST.get('last_name', '').capitalize()
        email_address = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        # Validate email format
        try:
            validate_email(email_address)
        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
            return redirect('signup')

        # Check if the email already exists
        if User.objects.filter(email=email_address).exists():
            messages.error(request, 'The email address provided already exists in our system. Please use a different email address or proceed to sign in.')
            return redirect('signup')

        otp = get_random_string(6, allowed_chars='0123456789')  # Generate 6-digit OTP

        # Store data in the session
        request.session['otp'] = otp  
        request.session['first_name'] = first_name  
        request.session['last_name'] = last_name  
        request.session['email'] = email_address  
        request.session['password'] = password  

        # Send email in the background
        # send_signup_email.delay(first_name, last_name, email_address, otp)

        subject = "SIGNUP VERIFICATION"
        html_content = render_to_string('email/signup_otp.html', {'first_name': first_name, 'last_name': last_name, 'otp': otp})
        email = EmailMessage(subject, html_content, settings.EMAIL_HOST_USER, [email_address])
        email.content_subtype = "html"
        email.send(fail_silently=False)

        messages.success(request, 'An OTP has been sent to your email address. Please check your inbox and enter the OTP to complete your registration.')
        return render(request,'auth/otp.html')  # Redirect immediately after initiating the email sending process
    
    return render(request, 'auth/signup.html')

def verify_signup_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')

        if entered_otp == session_otp:
            first_name = request.session.get('first_name', '').capitalize()
            last_name = request.session.get('last_name', '').capitalize()
            email_address = request.session.get('email')
            password = request.session.get('password')

            if email_address and password:
                try:
                    # Create and authenticate the user
                    user = User.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        username=email_address,
                        email=email_address,
                        password=password
                    )
                    login(request, user)

                    # Send email notification with user information
                    subject = "SUCCESSFUL SIGNUP"
                    html_content = render_to_string('email/signup_success.html', {'first_name': first_name, 'last_name': last_name})
                    email = EmailMessage(subject, html_content, settings.EMAIL_HOST_USER, [email_address])
                    email.content_subtype = "html"
                    email.send(fail_silently=False)

                    # Clear session data
                    request.session.flush()

                    messages.success(request, 'Congratulations! Your registration is complete. You are now logged in.')
                    return redirect('home')

                except Exception as e:
                    messages.error(request, f"There was an error completing your registration: {str(e)}")
            else:
                messages.error(request, 'Session data is incomplete. Please try signing up again.')

        else:
            messages.error(request, 'The OTP entered is invalid. Please try again.')

        return render(request, 'auth/otp.html')

    return redirect('signup')

def signin(request):
    # Redirect authenticated users directly to profile or home page
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Note the use of data=request.POST
        if form.is_valid():
            user = form.get_user()  # Get the user directly from the form
            login(request, user)
            messages.success(request, "You have successfully logged in. Welcome back!")
            return redirect('home')
        else:
            # Use Django's built-in form error handling
            messages.error(request, "Username or password is incorrect. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, "auth/signin.html", {'form': form})

@login_required
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Successfully logged out")
    else:
        messages.warning(request, "You are already logged out.")
    return redirect('home')
