
# Django
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings


class EmailService:
    
    @staticmethod
    def send_email(to_user, subject, template_name, context):

        template = get_template(template_name=template_name)

        content = template.render(context)

        message = EmailMultiAlternatives(
            subject=subject,
            body=content,
            from_email=settings.EMAIL_HOST_USER,
            to=[to_user.email]
        )

        message.content_subtype = 'html'
        message.send()