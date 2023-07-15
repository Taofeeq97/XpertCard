# Django imports
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.utils.text import slugify
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry
# Local imports
from .models import CompanyAddress, ActivityLog
from .models import LOGIN, LOGIN_FAILED


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
    ActivityLog.objects.create(actor=user, action_type=LOGIN)


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    message = f"Login Attempt Failed for email {credentials.get('email')} with ip: {get_client_ip(request)}"
    ActivityLog.objects.create(action_type=LOGIN_FAILED)


# @receiver(post_save)
# def update_document(sender, **kwargs):
#     app_label = sender._meta.app_label
#     model_name = sender._meta.model_name
#     instance = kwargs['instance']

#     if app_label == 'card':
#         if model_name == 'Expertcard':
#             instances = instance.article.all()
#             for _instance in instances:
#                 registry.update(_instance)


# @receiver(post_delete)
# def delete_document(sender, **kwargs):
#     app_label = sender._meta.app_label
#     model_name = sender._meta.model_name
#     instance = kwargs['instance']

#     if app_label == 'card':
#         if model_name == 'Expertcard':
#             instances = instance.article.all()
#             for _instance in instances:
#                 registry.update(_instance)
