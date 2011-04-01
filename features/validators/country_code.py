from django.core.exceptions import ValidationError

from simple_locations.models import Area

def validate(code):
    """
        Check if an Area with the given coutry code exists and raise
        a ValidationError otherwise.
    """
    code=code.upper()
    if not Area.objects.filter(two_letter_iso_country_code=code).exists():
        raise ValidationError(u"The country %s does not exist. " % code)
