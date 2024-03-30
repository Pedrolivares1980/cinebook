from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Cinema

# CreateView to add a new Cinema. Requires the user to be logged in and to be a staff member.
class CinemaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Cinema 
    fields = ['name', 'address', 'phone_number']
    template_name = 'cinemas/cinema_form.html' 
    success_url = reverse_lazy('admin_dashboard') 

    def test_func(self):
        return self.request.user.is_staff 

# UpdateView to update an existing Cinema. Requires the user to be logged in and to be a staff member.
class CinemaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Cinema  
    fields = ['name', 'address', 'phone_number'] 
    template_name = 'cinemas/cinema_form.html' 
    success_url = reverse_lazy('admin_dashboard')  

    def test_func(self):
        return self.request.user.is_staff 

# DeleteView to delete an existing Cinema. Requires the user to be logged in and to be a staff member.
class CinemaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Cinema 
    template_name = 'cinemas/cinema_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard') 

    def test_func(self):
        return self.request.user.is_staff 
