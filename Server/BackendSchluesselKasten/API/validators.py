from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible


@deconstructible
class HouseValidator():
    def __init__(self, exclude):
        self.exclude = exclude

    def __call__(self, value):
        value = self.clean(value)
        if value in self.exclude:
            raise ValidationError(
                _("Haus %(house)s existiert nicht"), params={"house": value})

    def __eq__(self, other):
        return self.exclude == other.exclude

    def clean(self, x):
        return x
