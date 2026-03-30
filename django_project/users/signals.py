from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
import logging
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

# These signals automatically create a Profile whenever a new User is made,
# and make sure the Profile is saved whenever the User is saved.



audit_logger = logging.getLogger('audit')

# This flag ensures signals are only connected once per process
if not hasattr(audit_logger, "_signals_connected"):
    audit_logger._signals_connected = True

    @receiver(user_logged_in)
    def log_user_login(sender, request, user, **kwargs):
        audit_logger.info(f"Successful login: {user.username}")

    @receiver(user_logged_out)
    def log_user_logout(sender, request, user, **kwargs):
        audit_logger.info(f"Logout: {user.username}")


    _failed_requests = set() # The incorrect login part records the same thing twice for no reason so this is here to stop that
    @receiver(user_login_failed)
    def log_user_login_failed(sender, credentials, request, **kwargs):
        # Use request object ID to uniquely identify a login attempt
        req_id = id(request)
        if req_id in _failed_requests:
            return  # Already logged this attempt

        _failed_requests.add(req_id)
        username = credentials.get('username', '<unknown>')
        audit_logger.info(f"Failed login attempt: {username}")