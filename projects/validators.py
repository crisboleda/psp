
# Django
from django.core.exceptions import ValidationError

# Utils
from projects.utils import MIN_LENGTH_INPUT_DESCRIPTION


def validate_min_length_description(value):
    if len(value) >= MIN_LENGTH_INPUT_DESCRIPTION:
        return value
    raise ValidationError("La cantidad minima de caracteres es {}".format(MIN_LENGTH_INPUT_DESCRIPTION))