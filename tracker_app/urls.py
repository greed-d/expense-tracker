from django.urls import path

from tracker_app.amount_input_form import ExpenseAmountInputView, IncomeAmountInputView
from tracker_app.views.add_category import AddCategoryView
from tracker_app.views.dashboard import UserDashboardView
from tracker_app.views.date_filter import DateFilterView, ExpenseTableView, IncomeTableView
from tracker_app.views.landing import HeroSectionView
from tracker_app.views.login_register import UserLoginView, UserRegisterView, UserLogoutView
from tracker_app.views.all_transactions import TransactionView

urlpatterns = [
    path("user_register/", UserRegisterView.as_view(), name="user_register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("addcategory/", AddCategoryView.as_view(), name="addcategory"),
    path("filter/", DateFilterView.as_view(), name="date-filter"),
    path("income_table/", IncomeTableView.as_view(), name="income_table"),
    path("expense_table/", ExpenseTableView.as_view(), name="expense_table"),
    path("transactions/", TransactionView.as_view(), name="transactions"),
    path("add_income_amount/", IncomeAmountInputView.as_view(), name="add_income_amount"),
    path("add_expense_amount/", ExpenseAmountInputView.as_view(), name="add_expense_amount"),
    path("home/", UserDashboardView.as_view(), name="home"),
    path("", HeroSectionView.as_view(), name="hero"),
]
