from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

@shared_task
def send_signup_email(first_name, last_name, email_address, otp):
    subject = "SIGNUP VERIFICATION"
    html_content = render_to_string('email/signup_otp.html', {'first_name': first_name, 'last_name': last_name, 'otp': otp})
    
    email = EmailMessage(subject, html_content, settings.EMAIL_HOST_USER, [email_address])
    email.content_subtype = "html"
    email.send(fail_silently=False)
