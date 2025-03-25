from rest_framework import serializers
from subscription.models import Subscriptions, Plan


class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscriptions
        fields = "__all__"
