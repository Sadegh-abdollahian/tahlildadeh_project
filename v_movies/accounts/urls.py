from django.urls import path, re_path
from .views import UserRegistrationView, UserVerifyView, LoginView, LogoutView

app_name = "blog"

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user_register"),
    path("verify/", UserVerifyView.as_view(), name="user_verify" ),
    path("login/", LoginView.as_view(), name="login" ),
    path("logout/", LogoutView.as_view(), name="logout" ),
    # path("buy_subscription", UserVerifyView.as_view(), name="buy_subscription"),
]
