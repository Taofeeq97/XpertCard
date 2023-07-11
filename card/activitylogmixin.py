# Django imports
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

# Local imports
from .models import ActivityLog, READ, CREATE, UPDATE, DELETE


class ActivityLogMixin:
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

    def _update_activity_log(self, instance, request):
        actor = self._get_user(request)
        message = f"modified {instance.first_name} {instance.last_name} expert's card"
        ActivityLog.objects.create(
            actor=actor,
            action_type=UPDATE,
            content_object=instance,
            data=message,
        )

    def _delete_activity_log(self, instance, request):
        actor = self._get_user(request)
        message = f"deleted {instance.first_name} {instance.last_name} expert's card"
        ActivityLog.objects.create(
            actor=actor,
            action_type=DELETE,
            content_object=instance,
            data=message,
        )

        