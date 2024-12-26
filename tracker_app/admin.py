from django.contrib import admin

from tracker_app.models import ExpenseCategory, ExpenseTracker, IncomeTracker

admin.site.register(IncomeTracker)
admin.site.register(ExpenseTracker)
admin.site.register(ExpenseCategory)
