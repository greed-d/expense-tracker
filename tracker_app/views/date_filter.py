
from django.db import models
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View

from tracker_app.forms import DateFilterForm
from tracker_app.models import ExpenseTracker, IncomeTracker

from tracker_app.views.dashboard import UserLoggedInMixin

class DateFilterView(UserLoggedInMixin, View):
    template_name = "tracker_app/date_filter.html"
    form_class = DateFilterForm

    def get_data(self, user):

        income_transactions = IncomeTracker.objects.filter(user=user ).values(
            'amount', 'source', 'reason', 'category__name', 'remarks', 'time'
        ).annotate(transaction_type=models.Value('Income', output_field=models.CharField()))

        expense_transactions = ExpenseTracker.objects.filter(user=user).values(
            'amount', 'source', 'reason', 'category__name', 'remarks', 'time'
        ).annotate(transaction_type=models.Value('Expense', output_field=models.CharField()))

        # Combine and sort by time

        return {
            "income_transactions" : income_transactions,
            "expense_transactions" : expense_transactions
        }
    
    def get(self, request):
        context_data = self.get_data(request.user)
        form = self.form_class
        context = {
            "form" : form,
            **context_data
        }
        return render(request, self.template_name, context=context)


    def post(self, request):
        context_data = self.get_data(request.user)
        form = self.form_class(request.POST)
        results = None

        try:

            if form.is_valid():
                start_date = form.cleaned_data["start_date"]
                end_date = form.cleaned_data["end_date"]
                source = form.cleaned_data["source"]
                input_type = form.cleaned_data["input_type"]

                filters = Q(user=request.user)

                if start_date:
                    filters &= Q(time__gte=start_date)
                if end_date:
                    filters &= Q(time__lte=end_date)
                if source:
                    filters &= Q(source=source)

                if input_type == "IN":
                    results = IncomeTracker.objects.filter(filters)
                elif input_type == "EX":
                    results = ExpenseTracker.objects.filter(filters)
            else:
                form.add_error(None, "Invalid form data, check data again")

        except Exception as e:
            print(f"An error occured {e}")
            form.add_error(None, "An error occured try again!!")

        context = {
            "form" : form,
            "results" : results,
            **context_data
        }
        return render(request, self.template_name, context=context)


