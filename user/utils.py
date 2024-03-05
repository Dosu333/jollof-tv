from django.core.mail import send_mail
from decouple import config

def send_password_reset_email(email_data):
    subject = 'Password Reset'
    client_url = config('CLIENT_URL')
    token = email_data['token']
    password_rest_url = f'{client_url}/password-rest/{token}'
    message = f'Hello {email_data["firstname"]},\n\n Below is the link to reset your password \n\n {password_rest_url}' 
    send_mail(
        subject,
        message,
        config('EMAIL_HOST'), 
        [email_data['email']],           
        fail_silently=False,        
    )