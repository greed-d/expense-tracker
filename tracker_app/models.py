from django.contrib.auth.models import User
from django.db import models

INCOME_AT = [("BA", "Bank"), ("WA", "Wallet"), ("CA", "Cash")]
INCOME_REASON = []

EXPENSE_FROM = [("Bank", "Bank"), ("Wallet", "Wallet"), ("Cash", "Cash")]

class ExpenseCategory(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE )
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"


class IncomeTracker(models.Model):
    amount = models.DecimalField(max_digits=12, default=0, decimal_places=2)
    source = models.CharField(max_length=50, choices=INCOME_AT)
    reason = models.CharField(max_length=50)
    remarks = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.source} - {self.amount}"



class ExpenseTracker(models.Model):
    amount = models.DecimalField(max_digits=12, default=0, decimal_places=2)
    source = models.CharField(max_length=50, choices=EXPENSE_FROM)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True)
    reason = models.CharField(max_length=200)
    remarks = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category} - {self.amount}"


