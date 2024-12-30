from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import FormView

from tracker_app.forms import UserLoginForm, UserRegsiterForm


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


class UserLoginView(FormView):
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

