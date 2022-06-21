from django.core.exceptions import ValidationError
import convert_numbers
from django.utils.translation import gettext_lazy as _


def check_phone_number(value):
    value = convert_numbers.persian_to_english(value)
    if len(value) > 11 or len(value) < 11:
        raise ValidationError(_('Invalid phone number.'))
    if not value.startswith('09'):
        raise ValidationError(_('Invalid phone number.'))
