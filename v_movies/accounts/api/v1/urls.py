from django.urls import path, re_path
from .views import UserRegisterView, UserVerifyView

app_name = "accounts"

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("verify/", UserVerifyView.as_view(), name="verify"),
]
