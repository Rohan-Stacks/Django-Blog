#I have added this py file python 3.13 is glitched with ssl and doesnt send emails,
# i got this description from another user with the same issue on reddit,

#"In Python 3.13, ssl.create_default_context() now uses VERIFY_X509_STRICT, and
#Python’s docs say that strict mode may reject pre-RFC 5280 or malformed certificates."

#By creating a subclass EmailBackend and refering it in setting.py i can override the
# ssl_context thing

import ssl
from django.core.mail.backends.smtp import EmailBackend

class RelaxedSMTPEmailBackend(EmailBackend):
    @property
    def ssl_context(self):
        context = ssl.create_default_context()
        context.verify_flags &= ~ssl.VERIFY_X509_STRICT
        return context