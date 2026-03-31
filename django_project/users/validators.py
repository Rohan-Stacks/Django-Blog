#Adding the password validator which enables a password requirement.

import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class StrongPasswordValidator:
    def validate(self, password, user=None):
        if not re.search(r"[A-Z]", password):
            raise ValidationError(_("Password must have 1 capital letter."), code="no_upper")

        if not re.search(r"[a-z]", password):
            raise ValidationError(_("Password must have 1 non-capital letter."), code="no_lower")

        if not re.search(r"\d", password):
            raise ValidationError(_("Password must have 1 number."), code="no_number")

        if not re.search(r"[^A-Za-z0-9]", password):
            raise ValidationError(_("Password must have 1 special character."), code="no_special")

    def get_help_text(self):
        return _(
            "Password must have 1 capital letter, 1 non-capital letter, 1 number, and 1 special character."
        )