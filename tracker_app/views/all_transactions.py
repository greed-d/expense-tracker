from itertools import chain

from django.db import models
from django.shortcuts import render
from django.views.generic.base import View

from tracker_app.models import ExpenseTracker, IncomeTracker

from django.contrib.auth.mixins import LoginRequiredMixin
class TransactionView(LoginRequiredMixin, View):
    template_name = "tracker_app/all_transactions.html"

    def get_data(self, user):

        income_transactions = IncomeTracker.objects.filter(user=user).values(
            'amount', 'source', 'reason', 'category__name', 'remarks', 'time'
        ).annotate(transaction_type=models.Value('Income', output_field=models.CharField()))

        expense_transactions = ExpenseTracker.objects.filter(user=user).values(
            'amount', 'source', 'reason', 'category__name', 'remarks', 'time'
        ).annotate(transaction_type=models.Value('Expense', output_field=models.CharField()))

        # Combine and sort by time
        recent_transactions = sorted(
            chain(income_transactions, expense_transactions),
            key=lambda x: x['time'],  # Use dictionary keys
            reverse=True
        )  # Limit to last 5 transactions

        return {
            "recent_transactions" : recent_transactions
        }
    
    def get(self, request):
        context_data = self.get_data(request.user)
        context = {
            **context_data
        }
        return render(request, self.template_name, context=context)
