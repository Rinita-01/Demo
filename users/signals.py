from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user': user,
        'full_name': f"{user.first_name} {user.last_name}",
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()

@receiver(user_logged_in)
def login_success_handler(sender, request, user, **kwargs):
    mail_subject = 'Login Successful - Notification'
    email_template = 'users/emails/user_logged_in.html'
    print(f"User: '{user.email}' has logged in successfully!")
    send_verification_email(request, user, mail_subject, email_template)
