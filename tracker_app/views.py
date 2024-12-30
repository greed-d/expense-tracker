from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.views.generic.base import View
from django.shortcuts import redirect, render
from django.db import models

from tracker_app.models import ExpenseTracker, IncomeTracker

from .forms import InputOrExpense, SourceFilterForm, UserLoginForm, UserRegsiterForm


class UserRegisterView(FormView):
    template_name = "tracker_app/user_register.html"
    form_class = UserRegsiterForm
    success_url = reverse_lazy("login")  # Redirect to the dashboard after registration

    def form_valid(self, form):
        username = self.request.POST["username"]
        first_name = self.request.POST["first_name"]
        print()
        print("-------------------------------")
        print(f"username = {username}, first_name = {first_name}")
        print("-------------------------------")
        print()
        # Save the user
        form.save()

        return super().form_valid(form)


class UserLoginStuff(FormView):
    template_name = "tracker_app/registration/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("home")
    # redirect_authenticated_user = True

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Invalid Credentials")
            return self.form_invalid(form)


class UserDashboardView(LoginRequiredMixin, View):
    template_name = "tracker_app/dashboard.html"
    form_class = InputOrExpense
    # success_url = reverse_lazy("home")

    def get(self, request):
        total_income = IncomeTracker.objects.filter(user=request.user).aggregate(models.Sum("amount"))["amount__sum"] or 0
        total_expense = ExpenseTracker.objects.filter(user=request.user).aggregate(models.Sum("amount"))["amount__sum"] or 0


        expense_category = (
        ExpenseTracker.objects.filter(user=request.user)
            .values("category__name")
            .annotate(Total_amount=models.Sum("amount"))
        )

        expense_source = (
            ExpenseTracker.objects.filter(user=request.user)
            .values("source")
            .annotate(total_sum=models.Sum("amount"))
        )

        current_balance = total_income - total_expense

        # Get form for filtering 
        filter_form = SourceFilterForm(request.GET)

        filtered_source = expense_source
        if filter_form.is_valid() and filter_form.cleaned_data["source"]:
            selected_source = filter_form.cleaned_data["source"]
            filtered_source = [item for item in expense_source if item["source"] == selected_source]



        #Debug Expressions
        print()
        print("------------------------------------")
        print(f"TOTAL_INCOME: {total_income}")
        print(f"TOTAL_EXPENSE: {total_expense}")
        print(f"TOTAL_EXPENSE: {expense_source}")
        print(f"CURRENT_BALANCE: {current_balance}")
        print(f"EXPENSE_CATEGORY : {expense_category}")
        # print(f"SOURCE : {self.form_class(request.POST).cleaned_data['source']}")
        print("------------------------------------")
        print()

        context = {
            "current_balance" : current_balance,
            "total_income": total_income,
            "total_expense": total_expense,
            "expense_total" : expense_source,
            "filtered_source": filtered_source,
            "filter_form": filter_form,
            # "expense_category" : expense_category,
            "form": InputOrExpense(),
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            input_type = form.cleaned_data["input_type"]
            amount = form.cleaned_data["amount"]
            source = form.cleaned_data["source"]
            reason = form.cleaned_data["reason"]
            remarks = form.cleaned_data["remarks"]

            if input_type == "IN":
                IncomeTracker.objects.create(
                    user = self.request.user,
                    amount = amount,
                    source = source,
                    reason = reason,
                    remarks = remarks
                )

            elif input_type == "EX":
                # category = form.cleaned_data["category"]
                ExpenseTracker.objects.create(
                    user = self.request.user,
                    amount = amount,
                    source = source,
                    # category = category,
                    reason = reason,
                    remarks = remarks,
                )
        return redirect("home")

    # def post(self, request):
    #     income_form = IncomeInputForm(request.POST)
    #     expense_form = ExpenseInputForm(request.POST)
    #
    #     selected_option = request.POST["form_selector"]
    #     print(f"User selected : {selected_option}")
    #
    #     if selected_option == "income":
    #         income = income_form.save(commit=False)
    #         income.user = request.user
    #         income.save()
    #         return redirect("home")
    #
    #     elif selected_option == "expense":
    #         expense = expense_form.save(commit=False)
    #         expense.user = request.user
    #         expense.save()
    #         return redirect("home")
            

        # if income_form.is_valid():
        #     income = income_form.save(commit=False)
        #     income.user = request.user
        #     income.save()
        #
        #     return redirect("home")
        # elif expense_form.is_valid():
        #     expense = expense_form.save(commit=False)
        #     expense.user = request.user
        #     expense.save()
        #
        #     return redirect("home")
        #
        #
        # 

        # TOTAL_INCOME = IncomeTracker.objects.filter(user=request.user).aggregate(models.Sum("amount"))["amount__sum"] or 0
        # TOTAL_EXPENSE = ExpenseTracker.objects.filter(user=request.user).aggregate(models.Sum("amount"))["amount__sum"] or 0
        #
        # current_balance = TOTAL_INCOME - TOTAL_EXPENSE
        #
        # context = {
        #     "current_balance" : current_balance,
        #     "total_income": TOTAL_INCOME,
        #     "total_expense": TOTAL_EXPENSE,
        #     "income_form": IncomeInputForm(),
        #     "expense_form": ExpenseInputForm()
        # }
        #
        # return render(request, self.template_name, context)




# class IncomeInputView(ListView):
#     model = IncomeTracker
#     template_name = "tracker_app/dashboard.html"
#     context_object_name = "income_input_view"
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.filter(user=self.request.user)


class HeroSectionView(TemplateView):
    template_name = "tracker_app/hero_section.html"

