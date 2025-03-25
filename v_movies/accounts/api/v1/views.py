from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from .serializers import PhoneNumberSerializer, RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from extensions.utils import send_otp
from random import randint
from accounts.models import OtpCode


class SendOTP(generics.CreateAPIView):
    serializer_class = PhoneNumberSerializer
    query_set = OtpCode.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        print(serializer)
        if serializer.is_valid():
            phone = serializer.validated_data.get("phone_number")
            otp = OtpCode.objects.filter(phone_number=phone).last()
            # Checks if the phone number is 11 numbers long
            if len(phone) != 11:
                return Response(
                    {"info": "phone_number is not valid"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Checks if otp is created or not
            if not otp:
                otp = randint(1000, 9999)
                OtpCode.objects.get_or_create(phone_number=phone, code=otp)
            send_otp(otp, phone)
            return Response({"info": "otp sent"}, status=status.HTTP_200_OK)
        return Response(
            {"info": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            otp = serializer.validated_data.get("otp")
            phone_number = serializer.validated_data.get("phone_number")
            obj = get_object_or_404(OtpCode, phone_number=phone_number, code=otp)
            obj.delete()
            return Response({"info": "user created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **Kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data.get("user")
            login(request, user)
            return Response(
                {"info": "logged in successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
