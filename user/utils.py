from django.core.mail import send_mail
from decouple import config

def send_password_reset_email(email_data):
    subject = 'Password Reset'
    password_rest_url = f'{config('CLIENT_URL')}/password-rest/{email_data['token']}'
    message = f'Hello {email_data["firstname"]},\n\n Below is the link to reset your password \n\n {password_rest_url}' 
    send_mail(
        subject,
        message,
        config('EMAIL_HOST'), 
        [email_data['email']],           
        fail_silently=False,        
    )