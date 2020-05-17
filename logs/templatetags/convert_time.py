
# Django
from django import template

register = template.Library()

@register.filter
def seconds_to_time(value):
    hours = int(value / 3600)
    minutes = int((value % 3600) / 60)
    seconds = int((value % 3600) % 60)

    return "{} Hr : {} Min : {} Seg".format(hours, minutes, seconds)