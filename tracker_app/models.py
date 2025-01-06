from django.contrib.auth.models import User
from django.db import models

INCOME_AT = [("BA", "Bank"), ("WA", "Wallet"), ("CA", "Cash")]

EXPENSE_FROM = [("BA", "Bank"), ("WA", "Wallet"), ("CA", "Cash")]

class ExpenseCategory(models.Model):
    user = models.ForeignKey(User,blank=True, null=True, on_delete=models.CASCADE )
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"


class IncomeTracker(models.Model):
    amount = models.DecimalField(max_digits=12, default=0, decimal_places=2)
    source = models.CharField(max_length=50, choices=INCOME_AT)
    reason = models.CharField(max_length=50)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, null=True, blank=True)
    remarks = models.TextField()
    time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.source} - {self.amount}"



class ExpenseTracker(models.Model):
    amount = models.DecimalField(max_digits=12, default=0, decimal_places=2)
    source = models.CharField(max_length=50, choices=EXPENSE_FROM)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True)
    reason = models.CharField(max_length=200)
    remarks = models.TextField()
    time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category} - {self.amount}"


