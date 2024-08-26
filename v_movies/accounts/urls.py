from django.urls import path, re_path
from .views import UserRegistrationView, UserVerifyView

app_name = "blog"

urlpatterns = [
    path("register", UserRegistrationView.as_view(), name="user_register" ),
    path("verify", UserVerifyView.as_view(), name="user_verify" ),
    path("buy_subscription", UserVerifyView.as_view(), name="buy_subscription" ),
]
