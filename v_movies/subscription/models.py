from django.db import models
from accounts.models import User
from django.utils import timezone


# Create your models here.
class Plan(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام")
    price_per_month = models.PositiveIntegerField(verbose_name="قیمت")
    # Counts by days (like 30 days or 60 days)
    credits_per_month = models.PositiveIntegerField(verbose_name="زمان اشتراک پلن")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["price_per_month"]
        verbose_name = "پلن"
        verbose_name_plural = "پلن ها"


class Subscriptions(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    subscription_start_timestamp = models.DateTimeField(default=timezone.now)
    subscription_end_timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.user.phone_number} - {self.plan.name}"

    class Meta:
        ordering = ("subscription_start_timestamp",)
        verbose_name = "اشتراک"
        verbose_name_plural = "اشتراک ها"
