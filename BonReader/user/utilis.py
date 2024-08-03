# utils.py
import random

def generate_6_digit_code():
    return str(random.randint(100000, 999999))

# custom_emails.py

from djoser import email
from .models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

class CustomActivationEmail(email.ActivationEmail):
    template_name = "emails/activations.html"

    def send(self, to, *args, **kwargs):
        context = self.get_context_data()
        user_id = context.get('user')
        user = User.objects.get(id=user_id.id)
        code = generate_6_digit_code()
        context["code"] = code
        user.activation_code = code
        user.save()
        
        try:
            # Render the email content with the updated context
            email_content = render_to_string(self.template_name, context)
            print("Rendered Email Content:", email_content)
            
            # Send the email using EmailMultiAlternatives
            subject = 'Activation Email'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]
            text_content = 'This is an important message.'
            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(email_content, "text/html")
            msg.send()
        except Exception as e:
            print("Error rendering email:", e)


class CustomPasswordResetEmail(email.PasswordResetEmail):
    template_name = "emails/activations.html"

    def send(self, to, *args, **kwargs):
        context = self.get_context_data()
        user = User.objects.get(email=to[0])
        code = generate_6_digit_code()
        context["code"] = code
        user.reset_code = code
        user.save()
