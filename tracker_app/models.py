from django.core.validators import BaseValidator
from django.db import models
from django.contrib.auth.models import User


INCOME_CHOICES = [("Bank", "Bank"), ("Wallet", "Wallet"), ("Cash", "Cash")]
INCOME_REASON = [("Bank", "Bank"), ("Wallet", "Wallet"), ("Cash", "Cash")]

EXPENSE_CHOICES = [("Bank", "Bank"), ("Wallet", "Wallet"), ("Cash", "Cash")]
EXPENSE_REASON = [
    ("Bank", "Bank-reason"),
    ("Wallet", "Wallet-reason"),
    ("Cash", "Cash-reason"),
]


class IncomeTracker(models.Model):
    source = models.CharField(max_length=50, choices=INCOME_CHOICES)
    amount = models.FloatField()
    reason = models.CharField(max_length=50, choices=INCOME_REASON)
    remarks = models.TextField()
    time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.reason


class ExpenseTracker(models.Model):
    source = models.CharField(max_length=50, choices=EXPENSE_CHOICES)
    amount = models.FloatField()
    reason = models.CharField(max_length=50, choices=EXPENSE_REASON)
    remarks = models.TextField()
    time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.reason


class ExpenseCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class IncomeCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
