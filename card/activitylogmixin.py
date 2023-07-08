# Python standard library imports
import logging

# Django imports
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

# Third-party imports
from rest_framework.exceptions import ValidationError

# Local imports
from .models import ActivityLog, READ, CREATE, UPDATE, DELETE, SUCCESS, FAILED

class ActivityLogMixin:
    log_message = None

    def _get_action_type(self, request) -> str:
        return self.action_type_mapper().get(request.method.upper())

    @staticmethod
    def action_type_mapper():
        return {
            "GET": READ,
            "PUT": UPDATE,
            "PATCH": UPDATE,
            "DELETE": DELETE,
        }

    @staticmethod
    def _get_user(request):
        user = request.user if request.user.is_authenticated else None
        return user

    def _write_log(self, request, response):
        status = SUCCESS if response.status_code < 400 else FAILED
        actor = self._get_user(request)

        if actor and not getattr(settings, "TESTING", False):
            logging.info("Started Log Entry")

            data = {
                "actor": actor,
                "action_type": self._get_action_type(request),
                "status": status,
            }
            try:
                data["content_type"] = ContentType.objects.get_for_model(self.get_queryset().model)
                data["content_object"] = self.get_object()
            except (AttributeError, ValidationError):
                data["content_type"] = None
            except AssertionError:
                pass
           
            object = self.get_object()
            print(object)
            message = f"{self._get_action_type(request)} {object.first_name} {object.last_name}'s Expert card"
            print(message)
            ActivityLog.objects.create(**data, data=message)

    def finalize_response(self, request, *args, **kwargs):
        print("Inside finalize_response")
        response = super().finalize_response(request, *args, **kwargs)
        self._write_log(request, response)
        return response


class ActivityLogCreateMixin:
    def _get_user(self, request):
        user = request.user if request.user.is_authenticated else None
        return user
    
    def _create_activity_log(self, instance, request):
        actor = self._get_user(request)
        message = f"created an expert's card for {instance.first_name} {instance.last_name}"
        ActivityLog.objects.create(
            actor=actor,
            action_type=CREATE,
            content_object=instance,
            data=message,
        )