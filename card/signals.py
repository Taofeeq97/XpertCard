from django.utils.text import slugify
from .models import CompanyAddress
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_login_failed
from .models import ActivityLog,  LOGIN, LOGIN_FAILED

@receiver(post_save, sender=CompanyAddress)
def generate_address_slug(sender, instance, **kwargs):
    if not instance.slug:
        slug = slugify(instance.address_title)
        instance.slug = slug
        instance.save()

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    return (
        x_forwarded_for.split(",")[0]
        if x_forwarded_for
        else request.META.get("REMOTE_ADDR")
    )


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    message = f"{user.first_name} is logged in with ip:{get_client_ip(request)}"
    ActivityLog.objects.create(actor=user, action_type=LOGIN, remarks=message)


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    message = f"Login Attempt Failed for email {credentials.get('email')} with ip: {get_client_ip(request)}"
    ActivityLog.objects.create(action_type=LOGIN_FAILED, remarks=message)