from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Cinema

# CreateView to add a new Cinema. Requires the user to be logged in and to be a staff member.
class CinemaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Cinema  # Specifies the model for which the form is created.
    fields = ['name', 'address', 'phone_number']  # Specifies the fields to be included in the form.
    template_name = 'cinemas/cinema_form.html'  # Specifies the template name to render the form.
    success_url = reverse_lazy('admin_dashboard')  # Specifies the URL to redirect to on successful form submission.

    def test_func(self):
        # This function tests if the current user is a staff member.
        return self.request.user.is_staff 

# UpdateView to update an existing Cinema. Requires the user to be logged in and to be a staff member.
class CinemaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Cinema  # Specifies the model for which the form is created.
    fields = ['name', 'address', 'phone_number']  # Specifies the fields to be included in the form.
    template_name = 'cinemas/cinema_form.html'  # Specifies the template name to render the form.
    success_url = reverse_lazy('admin_dashboard')  # Specifies the URL to redirect to on successful form submission.

    def test_func(self):
        # This function tests if the current user is a staff member.
        return self.request.user.is_staff 

# DeleteView to delete an existing Cinema. Requires the user to be logged in and to be a staff member.
class CinemaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Cinema  # Specifies the model to delete.
    template_name = 'cinemas/cinema_confirm_delete.html'  # Specifies the template used to confirm deletion.
    success_url = reverse_lazy('admin_dashboard')  # Specifies the URL to redirect to on successful deletion.

    def test_func(self):
        # This function tests if the current user is a staff member.
        return self.request.user.is_staff 
