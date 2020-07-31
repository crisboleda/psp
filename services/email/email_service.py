
# Django
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings


from mailjet_rest import Client
import os
import threading


class EmailService:

    @classmethod
    def send_email_production(cls, to_user, subject, template_name, context):
        api_key = settings.MAILJET_API_KEY
        api_secret = settings.MAILJET_API_SECRET

        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "carboleda64@misena.edu.co",
                        "Name": "Administrador"
                    },
                    "To": [
                        {
                            "Email": to_user.email,
                            "Name": to_user.username
                        }
                    ],
                    "Subject": "Welcome to PSP",
                    "TextPart": "Dear passenger 1, welcome to Mailjet! May the delivery force be with you!",
                    "HTMLPart": cls.get_content_html(template_name, context)
                }
            ]
        }

        thread = threading.Thread(target=mailjet.send.create, args=(data))
        thread.start()

    
    @classmethod
    def send_email_local(cls, to_user, subject, template_name, context):

        message = EmailMultiAlternatives(
            subject=subject,
            body=cls.get_content_html(template_name, context),
            from_email=settings.EMAIL_HOST_USER,
            to=[to_user.email]
        )

        message.content_subtype = 'html'
        message.send()


    @classmethod
    def get_content_html(cls, template_name, context):
        template = get_template(template_name=template_name)
        return template.render(context)