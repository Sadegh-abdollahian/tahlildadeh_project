from django.test import TestCase
from django.db.utils import IntegrityError
from subscription.models import Plan
from .factories import PlanFactory, SubscriptionsFactory, Subscriptions, UserFactory
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status


class PlanModelTests(TestCase):
    def setUp(self):
        # A sample Plan instance using Factory Boy
        self.plan = PlanFactory()

    def test_model_creation(self):
        """Test that a Plan instance is created successfully."""
        self.assertIsInstance(self.plan, Plan)
        self.assertEqual(self.plan.name, "برنزی")
        self.assertEqual(self.plan.price_per_month, 1_000_000)
        self.assertEqual(self.plan.credits_per_month, 30)

    def test_string_representation(self):
        """Test the __str__ method of the Plan model."""
        self.assertEqual(str(self.plan), "برنزی")

    def test_meta_options(self):
        """Test the Meta options of the Plan model."""
        meta = self.plan._meta
        self.assertEqual(meta.ordering, ["price_per_month"])
        self.assertEqual(meta.verbose_name, "پلن")
        self.assertEqual(meta.verbose_name_plural, "پلن ها")

    def test_name_max_length(self):
        """Test that the name field enforces its max_length constraint."""
        max_length = self.plan._meta.get_field("name").max_length
        self.assertEqual(max_length, 50)

    def test_price_per_month_positive(self):
        """Test that price_per_month must be a positive integer."""
        with self.assertRaises(IntegrityError):
            plan = PlanFactory(price_per_month=-1_000_000)
            plan.save()

    def test_credits_per_month_positive(self):
        """Test that credits_per_month must be a positive integer."""
        with self.assertRaises(IntegrityError):
            plan = PlanFactory(credits_per_month=-30)
            plan.save()

    def test_ordering(self):
        """Test that Plans are ordered by price_per_month."""
        # Create multiple plans with different prices
        PlanFactory(name="نقره‌ای", price_per_month=500_000, credits_per_month=15)
        PlanFactory(name="طلایی", price_per_month=2_000_000, credits_per_month=60)
        plans = Plan.objects.all()
        self.assertEqual(plans[0].price_per_month, 500_000)
        self.assertEqual(plans[1].price_per_month, 1_000_000)
        self.assertEqual(plans[2].price_per_month, 2_000_000)


class SubscriptionsModelTests(TestCase):
    def setUp(self):
        # A sample Subscription instance using Factory Boy
        self.subscription = SubscriptionsFactory()

    def test_model_creation(self):
        """Test that a Subscription instance is created successfully."""
        self.assertIsInstance(self.subscription, Subscriptions)
        self.assertEqual(self.subscription.user.username, "Jack")
        self.assertEqual(self.subscription.plan.name, "برنزی")
        self.assertEqual(
            self.subscription.subscription_start_timestamp.date(), timezone.now().date()
        )
        self.assertEqual(
            self.subscription.subscription_end_timestamp.date(),
            (timezone.now() + timezone.timedelta(days=30)).date(),
        )

    def test_subscription_start_end_timestamp(self):
        """Test that the subscription start and end timestamps are properly set."""
        self.assertTrue(
            self.subscription.subscription_start_timestamp
            <= self.subscription.subscription_end_timestamp
        )

    def test_string_representation(self):
        """Test the __str__ method of the Subscriptions model."""
        self.assertEqual(
            str(self.subscription),
            f"{self.subscription.user.phone_number} - {self.subscription.plan.name}",
        )

    def test_user_foreign_key(self):
        """Test that a Subscription is correctly linked to a User."""
        user = self.subscription.user
        self.assertEqual(user.username, "Jack")

    def test_plan_foreign_key(self):
        """Test that a Subscription is correctly linked to a Plan."""
        plan = self.subscription.plan
        self.assertEqual(plan.name, "برنزی")

    def test_unique_subscription_for_user(self):
        """Test that a user can only have one active subscription at a time."""
        # Create a user and an active subscription
        self.user = UserFactory()
        self.plan = PlanFactory()
        self.active_subscription = SubscriptionsFactory(
            user=self.user,
            plan=self.plan,
            subscription_end_timestamp=timezone.now() + timezone.timedelta(days=30),
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        subscription_data = {
            "plan": self.plan.id,
            "subscription_end_timestamp": timezone.now() + timezone.timedelta(days=30),
            "user": self.user.id,
        }
        response = self.client.post(
            "/subscription/api/v1/subscriptions/", subscription_data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            str(response.data["detail"]), "You do have an active subscription already."
        )

    def test_subscription_duration(self):
        """Test that the subscription duration is 30 days."""
        subscription_duration = (
            self.subscription.subscription_end_timestamp
            - self.subscription.subscription_start_timestamp
        )
        self.assertEqual(subscription_duration.days, 30)

    def test_subscription_user_plan_relation(self):
        """Test the relationship between a Subscription, User, and Plan."""
        user = self.subscription.user
        plan = self.subscription.plan
        self.assertEqual(self.subscription.user, user)
        self.assertEqual(self.subscription.plan, plan)

    def test_ordering_by_start_timestamp(self):
        """Test that Subscriptions are ordered by the start timestamp."""
        # Create multiple subscriptions
        SubscriptionsFactory(
            subscription_start_timestamp=timezone.now() - timezone.timedelta(days=5)
        )
        SubscriptionsFactory(
            subscription_start_timestamp=timezone.now() + timezone.timedelta(days=5)
        )
        subscriptions = Subscriptions.objects.all()

        # Check that they are ordered by subscription_start_timestamp
        self.assertTrue(
            subscriptions[0].subscription_start_timestamp
            <= subscriptions[1].subscription_start_timestamp
        )
        self.assertTrue(
            subscriptions[1].subscription_start_timestamp
            <= subscriptions[2].subscription_start_timestamp
        )

    def test_plan_credits_per_month_integrity(self):
        """Test that subscriptions cannot be created with invalid plan credits per month."""
        with self.assertRaises(IntegrityError):
            invalid_plan = PlanFactory(credits_per_month=-1)
            SubscriptionsFactory(plan=invalid_plan)
