from django.contrib.auth import login
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from tracker_app import forms


class UserRegisterView(FormView):
    template_name = "tracker_app/user_register.html"
    form_class = forms.UserRegsiterForm
    success_url = reverse_lazy(
        "dashboard"
    )  # Redirect to the dashboard after registration

    def form_valid(self, form):
        username = self.request.POST["username"]
        first_name = self.request.POST["first_name"]
        print()
        print("-------------------------------")
        print(f"username = {username}, first_name = {first_name}")
        print("-------------------------------")
        print()
        # Save the user
        form.save()

        return super().form_valid(form)


class UserDashboardView(TemplateView):
    template_name = "tracker_app/dashboard.html"
