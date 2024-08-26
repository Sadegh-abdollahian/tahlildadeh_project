from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django import forms
from .models import User


class SetPasswordMixin:
    """
    Form mixin that validates and sets a password for a user.

    This mixin also support setting an unusable password for a user.
    """

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    usable_password_help_text = _(
        "Whether the user will be able to authenticate using a password or not. "
        "If disabled, they may still be able to authenticate using other backends, "
        "such as Single Sign-On or LDAP."
    )

    @staticmethod
    def create_password_fields(label1=_("Password"), label2=_("Password confirmation")):
        password1 = forms.CharField(
            label=label1,
            required=False,
            strip=False,
            widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
            help_text=password_validation.password_validators_help_text_html(),
        )
        password2 = forms.CharField(
            label=label2,
            required=False,
            widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
            strip=False,
            help_text=_("Enter the same password as before, for verification."),
        )
        return password1, password2

    @staticmethod
    def create_usable_password_field(help_text=usable_password_help_text):
        return forms.ChoiceField(
            label=_("Password-based authentication"),
            required=False,
            initial="true",
            choices={"true": _("Enabled"), "false": _("Disabled")},
            widget=forms.RadioSelect(attrs={"class": "radiolist inline"}),
            help_text=help_text,
        )

    def validate_passwords(
        self,
        password1_field_name="password1",
        password2_field_name="password2",
        usable_password_field_name="usable_password",
    ):
        usable_password = (
            self.cleaned_data.pop(usable_password_field_name, None) != "false"
        )
        self.cleaned_data["set_usable_password"] = usable_password
        password1 = self.cleaned_data.get(password1_field_name)
        password2 = self.cleaned_data.get(password2_field_name)

        if not usable_password:
            return self.cleaned_data

        if not password1 and password1_field_name not in self.errors:
            error = ValidationError(
                self.fields[password1_field_name].error_messages["required"],
                code="required",
            )
            self.add_error(password1_field_name, error)

        if not password2 and password2_field_name not in self.errors:
            error = ValidationError(
                self.fields[password2_field_name].error_messages["required"],
                code="required",
            )
            self.add_error(password2_field_name, error)

        if password1 and password2 and password1 != password2:
            error = ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
            self.add_error(password2_field_name, error)

    def validate_password_for_user(self, user, password_field_name="password2"):
        password = self.cleaned_data.get(password_field_name)
        if password and self.cleaned_data["set_usable_password"]:
            try:
                password_validation.validate_password(password, user)
            except ValidationError as error:
                self.add_error(password_field_name, error)

    def set_password_and_save(self, user, password_field_name="password1", commit=True):
        if self.cleaned_data["set_usable_password"]:
            user.set_password(self.cleaned_data[password_field_name])
        else:
            user.set_unusable_password()
        if commit:
            user.save()
        return user


class UsernameField(forms.CharField):
    def to_python(self, value):
        value = super().to_python(value)
        if self.max_length is not None and len(value) > self.max_length:
            # Normalization can increase the string length (e.g.
            # "ﬀ" -> "ff", "½" -> "1⁄2") but cannot reduce it, so there is no
            # point in normalizing invalid data. Moreover, Unicode
            # normalization is very slow on Windows and can be a DoS attack
            # vector.
            return value
        return unicodedata.normalize("NFKC", value)

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "autocapitalize": "none",
            "autocomplete": "username",
        }


class BaseUserCreationForm(SetPasswordMixin, forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    password1, password2 = SetPasswordMixin.create_password_fields()
    usable_password = SetPasswordMixin.create_usable_password_field()

    class Meta:
        model = User
        fields = ("phone_number",)
        field_classes = {"phone_number": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = True

    def clean(self):
        self.validate_passwords()
        return super().clean()

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        self.validate_password_for_user(self.instance)

    def save(self, commit=True):
        user = super().save(commit=False)
        user = self.set_password_and_save(user, commit=commit)
        if commit and hasattr(self, "save_m2m"):
            self.save_m2m()
        return user


class UserCreationForm(BaseUserCreationForm):
    def clean_phone_number(self):
        """Reject phone_numbers that differ only in case."""
        phone_number = self.cleaned_data.get("phone_number")
        if (
            phone_number
            and self._meta.model.objects.get(phone_number__iexact=phone_number).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "phone_number": self.instance.unique_error_message(
                            self._meta.model, ["phone_number"]
                        )
                    }
                )
            )
        else:
            return phone_number


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see "
            "the user’s password."
        ),
    )

    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            if self.instance and not self.instance.has_usable_password():
                password.help_text = _(
                    "Enable password-based authentication for this user by setting a "
                    "password."
                )
        user_permissions = self.fields.get("user_permissions")
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related(
                "content_type"
            )


class UserRegistrationForm(forms.Form):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=11)
    about_me = forms.CharField(widget=forms.Textarea)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocompelete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocompelete": "new-password"}),
        help_text=("Enter the same password as before, for verification."),
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def clean_phone_number(self):
        """Reject phone_number that differ only in case."""
        phone_number = self.cleaned_data.get("phone_number")
        if (
            phone_number
            and self._meta.model.objects.filter(phone_number=phone_number).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "phone_number": self.instance.unique_error_message(
                            self._meta.model, ["phone_number"]
                        )
                    }
                )
            )
        else:
            return phone_number

    def clean_email(self):
        """Reject email that differ only in case."""
        email = self.cleaned_data.get("email")
        if email and self._meta.model.objects.filter(email=email).exists():
            self._update_errors(
                ValidationError(
                    {
                        "email": self.instance.unique_error_message(
                            self._meta.model, ["email"]
                        )
                    }
                )
            )
        else:
            return email


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()
