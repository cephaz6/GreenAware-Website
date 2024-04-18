from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def activate_account(user, email):
   try:
    # Generate a unique activation token
    activation_token = default_token_generator.make_token(user)

    # Build the activation link
    activation_link = reverse('activate', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': activation_token})

    # Send activation email
    subject = 'Activate Your Account'
    message = render_to_string('activation_email.html', {'activation_link': activation_link})
    send_mail(subject, message, 'cephasblog@gmail.com', [email])
   except Exception as e:
    print(e)

