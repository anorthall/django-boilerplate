from django.contrib import messages
from django.contrib.auth import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .forms import AuthenticationForm, PasswordChangeForm, RegistrationForm


class Index(views.TemplateView):
    template_name = "index.html"


class Register(views.FormView):
    template_name = "register.html"
    form_class = RegistrationForm

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, "Your account has been created. You can now log in."
        )
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.GET.get("next", "/")


class Login(SuccessMessageMixin, views.LoginView):
    success_message = "You are now logged in."
    template_name = "login.html"
    form_class = AuthenticationForm


class Logout(LoginRequiredMixin, views.LogoutView):
    def dispatch(self, *args, **kwargs):
        result = super().dispatch(*args, **kwargs)
        messages.success(self.request, "You have been logged out.")
        return result


class PasswordChangeView(
    SuccessMessageMixin, LoginRequiredMixin, views.PasswordChangeView
):
    success_message = "Your password has been changed."
    success_url = reverse_lazy("core:password_change")
    template_name = "password_change.html"
    form_class = PasswordChangeForm
