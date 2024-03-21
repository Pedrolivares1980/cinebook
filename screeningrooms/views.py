from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
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

# DeleteView for deleting a ScreeningRoom
class ScreeningRoomDeleteView(StaffRequiredMixin, DeleteView):
    model = ScreeningRoom
    template_name = 'screeningrooms/screeningroom_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard')

# ListView to show all ScreeningRooms
class ScreeningRoomListView(ListView):
    model = ScreeningRoom
    template_name = 'screeningrooms/screeningroom_list.html'

