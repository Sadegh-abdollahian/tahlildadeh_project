from rest_framework import viewsets, permissions, status, serializers
from .serializers import PlanSerializer, SubscriptionSerializer
from subscription.models import Plan, Subscriptions
from rest_framework.response import Response
from .zarinpal import send_request
from django.utils import timezone
from django.http import Http404
from rest_framework.exceptions import PermissionDenied
import datetime


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [permissions.AllowAny]


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # If user is superuser returns all the subscriptions
        if user.is_superuser:
            return Subscriptions.objects.all()
        # If user is not superuser returns user's subscriptions
        return Subscriptions.objects.filter(
            user=user, subscription_end_timestamp__gte=timezone.now()
        )

    def perform_create(self, serializer):
        # Checks if user has an active subscription otherwise continues
        if Subscriptions.objects.filter(
            user=self.request.user, subscription_end_timestamp__gte=timezone.now()
        ).exists():
            raise PermissionDenied("You do have an active subscription already.")
        # If no active subscription, continue creating the new one
        if serializer.is_valid():
            credits_per_month = serializer.validated_data["plan"].credits_per_month

            # Calculate the subscription end timestamp based on the plan's credits per month
            subscription_end_timestamp = timezone.now() + datetime.timedelta(
                days=credits_per_month
            )

            subscription = serializer.save(
                subscription_end_timestamp=subscription_end_timestamp,
                user=self.request.user,
            )

            return Response(
                SubscriptionSerializer(subscription).data,
                status=status.HTTP_201_CREATED,
            )

        else:
            raise serializers.ValidationError("Serializer is not valid")
