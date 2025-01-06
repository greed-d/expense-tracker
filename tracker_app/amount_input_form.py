
from django.shortcuts import render, redirect
from django.views.generic.base import View

from tracker_app.forms import ExpenseInputForm, IncomeInputForm
from tracker_app.views.dashboard import UserLoggedInMixin
from tracker_app.models import ExpenseTracker, IncomeTracker

class IncomeAmountInputView(UserLoggedInMixin, View):
    template_name = "tracker_app/income_input_form.html"
    form_class = IncomeInputForm

    def get(self, request):

        context = {
            "form" : self.form_class()
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            amount = form.cleaned_data["amount"]
            source = form.cleaned_data["source"]
            time = form.cleaned_data["time"]
            reason = form.cleaned_data["reason"]
            remarks = form.cleaned_data["remarks"]
            IncomeTracker.objects.create(
                user=self.request.user,
                amount=amount,
                source=source,
                time=time,
                reason=reason,
                remarks=remarks,
            )
            return redirect("add_income_amount")


class ExpenseAmountInputView(UserLoggedInMixin, View):
    template_name = "tracker_app/expense_input_form.html"
    form_class = ExpenseInputForm

    def get(self, request):

        context = {
            "form" : self.form_class(user=request.user)
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            print(f"expense foem {form}")
            amount = form.cleaned_data["amount"]
            source = form.cleaned_data["source"]
            time = form.cleaned_data["time"]
            reason = form.cleaned_data["reason"]
            remarks = form.cleaned_data["remarks"]
            category = form.cleaned_data["category"]

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
