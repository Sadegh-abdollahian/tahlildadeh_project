# Generated by Django 5.1 on 2024-10-09 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_user_phone_number_alter_user_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="has_supscription",
            field=models.BooleanField(default=False, verbose_name="آشتراک دارد"),
        ),
    ]
