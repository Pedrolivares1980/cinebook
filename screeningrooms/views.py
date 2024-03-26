from django.urls import reverse_lazy
from django.views.generic import  CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import ScreeningRoom
from .forms import ScreeningRoomForm


# Custom mixin to check if user is staff
class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

# CreateView for adding a new ScreeningRoom
class ScreeningRoomCreateView(StaffRequiredMixin, CreateView):
    model = ScreeningRoom
    form_class = ScreeningRoomForm
    template_name = 'screeningrooms/screeningroom_form.html'
    success_url = reverse_lazy('admin_dashboard')

    # Set initial values and save with fixed seats per row
    def form_valid(self, form):
        response = super().form_valid(form)
        return response

# UpdateView for editing an existing ScreeningRoom
class ScreeningRoomUpdateView(StaffRequiredMixin, UpdateView):
    model = ScreeningRoom
    form_class = ScreeningRoomForm
    template_name = 'screeningrooms/screeningroom_form.html'
    success_url = reverse_lazy('admin_dashboard')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.object:  # Checks if an object is being updated
            form.fields['cinema'].disabled = True  # Disables the 'cinema' field
        return form

# DeleteView for deleting a ScreeningRoom
class ScreeningRoomDeleteView(StaffRequiredMixin, DeleteView):
    model = ScreeningRoom
    template_name = 'screeningrooms/screeningroom_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard')
