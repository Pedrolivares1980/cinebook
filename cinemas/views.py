from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Cinema


# CreateView for adding a new Cinema
class CinemaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Cinema
    fields = ['name', 'address', 'phone_number']
    template_name = 'cinemas/cinema_form.html' 
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return self.request.user.is_staff 

class CinemaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Cinema
    fields = ['name', 'address', 'phone_number'] 
    template_name = 'cinemas/cinema_form.html' 
    success_url = reverse_lazy('admin_dashboard') 
    def test_func(self):
        return self.request.user.is_staff 

# DeleteView for deleting a Cinema
class CinemaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Cinema
    template_name = 'cinemas/cinema_confirm_delete.html' 
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return self.request.user.is_staff 

class CinemaListView(ListView):
    model = Cinema
    template_name = 'cinemas/cinema_list.html'
