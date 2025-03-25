import factory
from django.utils import timezone
from subscription.models import Plan, Subscriptions
from accounts.models import User
from random import randint


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    phone_number = factory.LazyAttribute(lambda x: f"099610{randint(100000, 999999)}")
    username = "Jack"


class PlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Plan

    name = "برنزی"
    price_per_month = 1_000_000
    credits_per_month = 30


class SubscriptionsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscriptions

    user = factory.SubFactory(UserFactory)
    plan = factory.SubFactory(PlanFactory)
    subscription_start_timestamp = factory.LazyFunction(timezone.now)
    subscription_end_timestamp = factory.LazyFunction(
        lambda: timezone.now() + timezone.timedelta(days=30)
    )
