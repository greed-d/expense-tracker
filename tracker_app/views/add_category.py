from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.base import View

from tracker_app.forms import AddCategory
from tracker_app.models import ExpenseCategory


class AddCategoryView(View):
    template_name = "tracker_app/add_category.html"
    form_class = AddCategory

    def get(self, request):
        form = self.form_class
        categories = ExpenseCategory.objects.filter(user=request.user)

        context = {
            "form" : form,
            "categories": categories
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        print(f"From add category viewe : {request.POST}")
        form = self.form_class(request.POST)

        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": True, "category_id": category.id, "category_name": category.name})

            return redirect("addcategory")

        return render(request, self.template_name, {"form" : form})
