from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from tracker_app.models import IncomeTracker, ExpenseTracker


class UserRegsiterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

class UserLoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=20)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class InputOrExpense(forms.Form):
    input_type = forms.ChoiceField(
        choices=(("IN", "Income"), ("EX", "Expense")),
        widget=forms.Select,
        required=True
    )
    amount = forms.DecimalField(
        max_digits=12, 
        decimal_places=2,
        min_value=1,  # Ensure no negative amounts are entered
        required=True
    )
    source = forms.ChoiceField(
        choices=(("CA", "Cash"), ("BA", "Bank"), ("WA", "Wallet")),
        widget=forms.Select,
        required=True
    )
    reason = forms.CharField(
        max_length=200, 
        required=True
    )
    remarks = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter remarks (optional)"} ), 
        required=False
    )



class IncomeInputForm(forms.ModelForm):
    class Meta:
        model = IncomeTracker
        fields = ["amount", "source", "reason", "remarks"]


class ExpenseInputForm(forms.ModelForm):
    class Meta:
        model = ExpenseTracker
        fields = ["amount", "source", "reason", "remarks"]
