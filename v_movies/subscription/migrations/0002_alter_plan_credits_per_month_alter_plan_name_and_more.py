# Generated by Django 5.1 on 2025-03-06 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscription", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plan",
            name="credits_per_month",
            field=models.PositiveIntegerField(verbose_name="زمان اشتراک پلن"),
        ),
        migrations.AlterField(
            model_name="plan",
            name="name",
            field=models.CharField(max_length=50, verbose_name="نام"),
        ),
        migrations.AlterField(
            model_name="plan",
            name="price_per_month",
            field=models.PositiveIntegerField(verbose_name="قیمت"),
        ),
    ]
