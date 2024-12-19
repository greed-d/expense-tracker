from django import forms
from django.contrib.auth.models import User


class UserRegsiterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "password",
            "confirm_password",
            "email",
        ]

    # def clean_data
