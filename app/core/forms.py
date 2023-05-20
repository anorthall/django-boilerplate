from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Submit
from django import forms
from django.contrib import auth
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import AppUser


class AuthenticationForm(auth.forms.AuthenticationForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "mb-4"
        self.helper.form_show_errors = False
        self.helper.layout = Layout(
            Div(
                Div(
                    FloatingField("username"),
                    css_class="col-12",
                ),
                Div(
                    FloatingField("password"),
                    css_class="col-12",
                ),
                Div(
                    Submit("submit", "Submit", css_class="btn-lg h-100 w-100"),
                    css_class="col-12",
                ),
                css_class="row",
            )
        )


class PasswordChangeForm(auth.forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "mb-4"
        self.helper.layout = Layout(
            Div(
                Div(
                    FloatingField("old_password"),
                    css_class="col-12",
                ),
                Div(
                    FloatingField("new_password1"),
                    css_class="col-12",
                ),
                Div(
                    FloatingField("new_password2"),
                    css_class="col-12",
                ),
                Div(
                    Submit("submit", "Change password", css_class="btn-lg h-100 w-100"),
                    css_class="col-12",
                ),
                css_class="row",
            )
        )


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = AppUser
        fields = [
            "email",
            "name",
            "is_active",
        ]


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = AppUser
        fields = [
            "email",
            "name",
            "password1",
            "password2",
            "is_active",
            "is_superuser",
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:  # pragma: no cover
            user.save()
        return user


class RegistrationForm(UserCreationForm):
    class Meta:
        model = AppUser
        fields = [
            "email",
            "name",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "mb-4"
        self.helper.layout = Layout(
            Div(
                Div(
                    FloatingField("email"),
                    css_class="col-12",
                ),
                Div(
                    FloatingField("name"),
                    css_class="col-12",
                ),
                Div(
                    FloatingField("password1"),
                    css_class="col-12",
                ),
                Div(
                    FloatingField("password2"),
                    css_class="col-12",
                ),
                Div(
                    Submit("submit", "Register", css_class="btn-lg h-100 w-100"),
                    css_class="col-12",
                ),
                css_class="row",
            )
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        if commit:  # pragma: no cover
            user.save()
        return user
