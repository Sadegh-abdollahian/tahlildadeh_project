from rest_framework import permissions
from subscription.models import Subscriptions
from django.utils import timezone


class UniqueSubscriptionPermission(permissions.BasePermission):
    """
    Checks if user has an active permission
    """

    def has_object_permission(self, request, view, obj):

        if Subscriptions.objects.filter(
            user=request.user, subscription_end_timestamp__gte=timezone.now()
        ).exists():
            return False

        return True
