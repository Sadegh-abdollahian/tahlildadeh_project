# Generated by Django 5.1 on 2024-10-18 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_alter_user_has_supscription"),
    ]

    operations = [
        migrations.CreateModel(
            name="OtpCode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("phone_number", models.CharField(max_length=11)),
                ("code", models.CharField(max_length=6)),
            ],
        ),
    ]
