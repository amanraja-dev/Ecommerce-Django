from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User , auth
import random
import string
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# from premailer import transform
    
def forget_password(request):
    return render(request, 'auth/forget.html')

def reset_password_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        
        user = User.objects.get(email=email)
        if User.objects.filter(email=user.email).exists():
            # Generate OTP
            otp = ''.join(random.choices(string.digits, k=6))  # 6-digit OTP example
            
            # Store OTP in the session
            request.session['reset_password_otp'] = otp
            request.session['reset_password_email'] = email
            
            subject = "Password Reset OTP"
            message = f"Hi {user.first_name} {user.last_name},\n\n" \
                      f"Your OTP for resetting the password on OURSHOP website is: {otp}\n\n" \
                      "Please use this OTP to reset your password. This OTP is valid for a limited time.\n\n" \
                      "Best regards,\n" \
                      "OURSHOP Team"

            # Send OTP to the provided email address
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,  # Sender's email
                [email],
                fail_silently=False,
            )

            # For simplicity, assuming OTP sending is successful
            return JsonResponse({'success': True, 'otp': otp})
        else:
            return JsonResponse({'success': False, 'error': 'Email not registered'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
def verify_reset_password_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        # Retrieve OTP from the session
        expected_otp = request.session.get('reset_password_otp')
        reset_email = request.session.get('reset_password_email')
        if otp == expected_otp:
            # OTP verified successfully
            # Optionally, you can clear the OTP from the session
            request.session.flush()
            user = User.objects.get(email=reset_email)
            return redirect('login')
        else:
            # Invalid OTP
            messages.error(request, 'Invalid OTP')
            return redirect('forget_password')
    else:
        # Invalid request method
        return JsonResponse({'success': False, 'error': 'Invalid request method'})