from django.shortcuts import redirect
from .serializers import RegisterSerializer, VerifySerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from random import randint
from extensions.utils import send_opt
from accounts.models import User, OtpCode


# Create your views here.
class UserRegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request: Request):
        data = request.data

        data["password"] = make_password(data["password"])

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            code = randint(100000, 999999)
            phone_number = data["phone_number"]
            send_opt(code, phone_number)
            OtpCode.objects.create(phone_number=phone_number, code=code)
            request.session["user_registration_info"] = {
                "phone_number": phone_number,
                "username": serializer.data["username"],
                "password": serializer.data["password"],
            }

            response = {
                "message": "User has saved to temporary memory",
                "data": serializer.data,
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVerifyView(generics.GenericAPIView):
    serializer_class = VerifySerializer

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        user_session = request.session["user_registration_info"]
        code_instance = OtpCode.objects.get(phone_number=user_session["phone_number"])

        if serializer.is_valid():
            code = serializer.data["code"]
            if code == code_instance.code:
                user = User(
                    phone_number=serializer.data["phone_number"],
                    username=serializer.data["username"],
                )
                user.set_password(user_session["password"])
                user.save()
                code_instance.delete()
                user = authenticate(
                    request,
                    phone_number=user_session["phone_number"],
                    password=user.password,
                )
                if user is not None:
                    login(request, user)
                del request.session["user_registration_info"]
