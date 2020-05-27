
# Django
from django import template
from django.template.loader import get_template, select_template

register = template.Library()


# Limpia un dato de la sesión
@register.filter
def clear_session_data(session, value):
    if value in session:
        del session[value]
    return ""


@register.inclusion_tag('alert_success.html')
def show_alert_success(value):
    return {
        'description': value
    }
