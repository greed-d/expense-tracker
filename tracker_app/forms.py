from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from tracker_app.models import ExpenseCategory


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

class AddCategory(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ["name"]

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
    category = forms.ModelChoiceField(
        queryset = ExpenseCategory.objects.all(),
        widget = forms.Select,
        required=True,
        empty_label="Select Category",
    )
    time = forms.DateTimeField(
        label = "When?",
        widget = forms.DateTimeInput(attrs={'type' : 'datetime-local'}),
        input_formats = ["%Y-%m-%dT%H:%M"]
    )
    reason = forms.CharField(
        max_length=200, 
        required=True
    )
    remarks = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Enter remarks (optional)",
            "rows": 2  
        }),
        required=False
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(InputOrExpense, self).__init__(*args, **kwargs)
        print(ExpenseCategory.objects.filter(user=user))
        self.fields["category"].choices = tuple(ExpenseCategory.objects.filter(user=user).values_list("id", "name"))
        print(self.fields["category"].choices)

class SourceFilterForm(forms.Form):
    type = forms.ChoiceField(
        choices=(("IN", "Income"), ("EX", "Expense")),
        widget=forms.Select,
    )
    source = forms.ChoiceField(
        choices=(("CA", "Cash"), ("BA", "Bank"), ("WA", "Wallet")),
        widget=forms.Select,
    )
