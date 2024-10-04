from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, VerifyCodeForm, LoginForm
from django.views import View
from django.contrib.auth import authenticate, login, logout
from random import randint
from extensions.utils import send_opt
from .models import User, OtpCode
from django.http import Http404

# Create your views here.

class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_name = "accounts/register.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            code = randint(1000, 9999)
            cd = form.cleaned_data
            phone_number = cd["phone_number"]
            send_opt(code, phone_number)
            OtpCode.objects.create(phone_number=phone_number, code=code)
            request.session["user_registration_info"] = {
                "phone_number": phone_number,
                "email": cd["email"],
                "first_name": cd["first_name"],
                "last_name": cd["last_name"],
                "password": cd["password2"],
            }
            return redirect("accounts:user_verify")
        return render(request, self.template_name, {"form": form})


class UserVerifyView(View):
    form_class = VerifyCodeForm
    template_name = "accounts/verify.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.session["user_registration_info"]:
            user_session = request.session["user_registration_info"]
        else:
            return Http404
        code_instance = OtpCode.objects.filter(phone_number=user_session["phone_number"])[0]
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            if code == code_instance.code:
                User.objects.create(
                    phone_number=user_session["phone_number"],
                    email=user_session["email"],
                    first_name=user_session["first_name"],
                    last_name=user_session["last_name"],
                    password=user_session["password"],
                )
                code_instance.delete()
                del request.session["user_registration_info"]
                return redirect("/contents")
            else:
                return Http404
        return render(request, self.template_name, {"form": form})

class LoginView(View):
    form_class = LoginForm
    template_name = "accounts/login.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            user2 = authenticate(request, first_name="sadegh@gmail.com")
            user = authenticate(request, phone_number=phone_number, password=password)
            print("user :", user)
            print("number :", phone_number)
            print("password :", password)
            print("User 2 :", user2)
            if user is not None:
                login(request, user)
                return redirect("/contents")
        return render(request, self.template_name, {"form": form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/contents")
