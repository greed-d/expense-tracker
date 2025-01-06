from itertools import chain
from django.core.paginator import Paginator

from django.db import models
from django.shortcuts import render
from django.views.generic.base import View

from tracker_app.models import ExpenseTracker, IncomeTracker

from django.contrib.auth.mixins import LoginRequiredMixin
class TransactionView(LoginRequiredMixin, View):
    template_name = "tracker_app/all_transactions.html"
    paginate_by = 7

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
            key=lambda x: x['time'],
            reverse=True
        )

        return recent_transactions
        
    
    def get(self, request):
        transactions = self.get_data(request.user)

        paginator = Paginator(transactions, self.paginate_by)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj" : page_obj,
            "is_paginated" : page_obj.has_other_pages()
            # **transactions
        }
        return render(request, self.template_name, context=context)
