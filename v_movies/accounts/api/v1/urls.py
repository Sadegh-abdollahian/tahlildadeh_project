from django.urls import path
from .views import SendOTP, RegisterView

urlpatterns = [
    path("send_otp/", SendOTP.as_view(), name="send_otp"),
    path("register/", RegisterView.as_view(), name="register"),
]
