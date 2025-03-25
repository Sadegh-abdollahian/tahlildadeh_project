from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone_number(value):
    if len(value) != 11:
        raise ValidationError(
            _("%(value)s is not a valid phone number"),
            params={"value": value},
        )
