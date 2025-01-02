from itertools import chain

from django.db import models
from django.shortcuts import redirect, render
from django.views.generic.base import View

from tracker_app.forms import InputOrExpense, SourceFilterForm
from tracker_app.models import ExpenseTracker, IncomeTracker


class UserLoggedInMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)


class UserDashboardView(UserLoggedInMixin, View):
    template_name = "tracker_app/dashboard.html"
    form_class = InputOrExpense
    filter_result = None

    def get_data(self, user):
        total_income = (
            IncomeTracker.objects.filter(user=user).aggregate(models.Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )
        total_expense = (
            ExpenseTracker.objects.filter(user=user).aggregate(models.Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )

        current_balance = total_income - total_expense

        income_transactions = (
            IncomeTracker.objects.filter(user=user)
            .values("amount", "source", "reason", "category__name", "remarks", "time")
            .annotate(
                transaction_type=models.Value("Income", output_field=models.CharField())
            )
        )

        expense_transactions = (
            ExpenseTracker.objects.filter(user=user)
            .values("amount", "source", "reason", "category__name", "remarks", "time")
            .annotate(
                transaction_type=models.Value(
                    "Expense", output_field=models.CharField()
                )
            )
        )

        # Combine and sort by time
        recent_transactions = sorted(
            chain(income_transactions, expense_transactions),
            key=lambda x: x["time"],  # Use dictionary keys
            reverse=True,
        )[:5]  # Limit to last 5 transactions

        return {
            "current_balance": current_balance,
            "total_income": total_income,
            "total_expense": total_expense,
            "recent_transactions": recent_transactions,
        }

    def get(self, request):
        context_data = self.get_data(request.user)

        # Get form for filtering
        filter_form = SourceFilterForm()

        context = {
            "filter_form": filter_form,
            "form": InputOrExpense(user=request.user),
            **context_data,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        context_data = self.get_data(request.user)
        form = self.form_class(request.POST)
        filter_form = SourceFilterForm(request.POST)

        filter_result = None

        print(request.POST)

        # breakpoint()
        if "tracker_submit" in request.POST:
            if form.is_valid():
                input_type = form.cleaned_data["input_type"]
                amount = form.cleaned_data["amount"]
                source = form.cleaned_data["source"]
                time = form.cleaned_data["time"]
                reason = form.cleaned_data["reason"]
                remarks = form.cleaned_data["remarks"]
                category = form.cleaned_data["category"]

                print()
                print("-------------------------")
                # print(f"Form is : { form }")
                print(f"Input Type : {input_type}")
                print(f"Amount : {amount}")
                print(f"Source : {source}")
                print(f"Category : {category}")
                # print(time)
                print("-------------------------")
                print()

                if input_type == "IN":
                    IncomeTracker.objects.create(
                        user=self.request.user,
                        amount=amount,
                        source=source,
                        time=time,
                        reason=reason,
                        remarks=remarks,
                    )

                elif input_type == "EX":
                    # category = form.cleaned_data["category"]
                    ExpenseTracker.objects.create(
                        user=self.request.user,
                        amount=amount,
                        source=source,
                        time=time,
                        category=category,
                        reason=reason,
                        remarks=remarks,
                    )
                return redirect("home")

        elif "filter_submit" in request.POST:
            if filter_form.is_valid():
                search_type = filter_form.cleaned_data["type"]
                print(search_type)

                if search_type == "IN":
                    selected_source = filter_form.cleaned_data["source"]
                    print(f"selected_source : {selected_source}")
                    filter_result = IncomeTracker.objects.filter(
                        user=request.user, source=selected_source
                    ).values("amount", "reason", "category__name", "remarks")
                    # filter_result = IncomeTracker.objects.filter(user=request.user, source=selected_source)
                    print(f"Incom filter result {filter_result}")

                elif search_type == "EX":
                    selected_source = filter_form.cleaned_data["source"]
                    print(f"Expense Source {selected_source}")
                    filter_result = ExpenseTracker.objects.filter(
                        user=request.user, source=selected_source
                    ).values("amount", "reason", "category__name", "remarks")
                    # filter_result = ExpenseTracker.objects.filter(user=request.user, source=selected_source)

        else:
            print("Form is invalid. Errors:")
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field '{field}': {error}")
            print("Non-field errors:", form.non_field_errors())

        context = {
            "form": self.form_class(user=request.user),
            "filter_form": filter_form,
            "filter_result": filter_result,
            **context_data,
        }

        return render(request, self.template_name, context=context)
