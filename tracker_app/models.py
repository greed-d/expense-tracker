from django.contrib.auth.models import User
from django.db import models

INCOME_AT = [("BA", "Bank"), ("WA", "Wallet"), ("CA", "Cash")]
INCOME_REASON = []

EXPENSE_FROM = [("Bank", "Bank"), ("Wallet", "Wallet"), ("Cash", "Cash")]


class IncomeTracker(models.Model):
    amount = models.DecimalField(max_digits=12, default=0, decimal_places=2)
    source = models.CharField(max_length=50, choices=INCOME_AT)
    reason = models.CharField(max_length=50)
    remarks = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.reason


# class UserBalance(models.Model):
#     current_amount = models.DecimalField(max_digits=12, default=0, decimal_places=2)
#     income_amount = models.DecimalField(max_digits=12, default=0, decimal_places=2)
#     expense_amount = models.DecimalField(max_digits=12, default=0, decimal_places=2)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)


class ExpenseTracker(models.Model):
    amount = models.DecimalField(max_digits=12, default=0, decimal_places=2)
    source = models.CharField(max_length=50, choices=EXPENSE_FROM)
    reason = models.CharField(max_length=200)
    remarks = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.reason


class ExpenseCategory(models.Model):
    # default = ["Entertainment", "Transportation", "Food"]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
