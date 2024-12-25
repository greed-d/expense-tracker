from django.contrib import admin

from tracker_app.models import ExpenseTracker, IncomeTracker

admin.site.register(IncomeTracker)
admin.site.register(ExpenseTracker)
