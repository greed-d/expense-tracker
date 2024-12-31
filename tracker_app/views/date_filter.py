from django.db.models import Q
from django.views.generic.base import View
from django.shortcuts import render
from tracker_app.forms import DateFilterForm
from tracker_app.models import IncomeTracker

class DateFilterView(View):
    template_name = "tracker_app/date_filter.html"
    form_class = DateFilterForm

    def get(self, request):
        form = self.form_class
        context = {
            "form" : form
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = self.form_class(request.POST)
        results = None

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
                results = IncomeTracker.objects.filter(filters)

        context = {
            "form" : form,
            "results" : results
        }
        return render(request, self.template_name, context=context)


