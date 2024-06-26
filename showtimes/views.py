from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ShowtimeForm
from django.urls import reverse_lazy
from .models import Showtime
from .forms import ShowtimeFilterForm
from django.utils import timezone


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class ShowtimeCreateView(StaffRequiredMixin, CreateView):
    model = Showtime
    form_class = ShowtimeForm 
    template_name = 'showtimes/showtime_form.html'
    success_url = reverse_lazy('admin_dashboard')

class ShowtimeUpdateView(StaffRequiredMixin, UpdateView):
    model = Showtime
    form_class = ShowtimeForm 
    template_name = 'showtimes/showtime_form.html'
    success_url = reverse_lazy('admin_dashboard')

class ShowtimeDeleteView(StaffRequiredMixin, DeleteView):
    model = Showtime
    template_name = 'showtimes/showtime_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard')

class ShowtimeListView(ListView):
    model = Showtime
    template_name = 'showtimes/showtime_list.html'
    context_object_name = 'showtimes'
    paginate_by = 6 

    def get_queryset(self):
        queryset = Showtime.objects.filter(showtime__gte=timezone.now()).order_by('showtime')

        form = ShowtimeFilterForm(self.request.GET)
        if form.is_valid():
            cinema = form.cleaned_data.get('cinema')
            screening_room = form.cleaned_data.get('screening_room')
            movie = form.cleaned_data.get('movie')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            if cinema:
                queryset = queryset.filter(screening_room__cinema=cinema)
            if screening_room:
                queryset = queryset.filter(screening_room=screening_room)
            if movie:
                queryset = queryset.filter(movie=movie)
            if start_date:
                queryset = queryset.filter(showtime__gte=start_date)
            if end_date:
                queryset = queryset.filter(showtime__lte=end_date)

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        showtimes = context['showtimes']
        
        showtimes_with_seat_info = [
            {
                'showtime': showtime,
                'total_seats': showtime.screening_room.seats.count(),
                'available_seats': showtime.available_seats()
            }
            for showtime in showtimes
        ]
        
        context['showtimes_with_seat_info'] = showtimes_with_seat_info
        context['filter_form'] = ShowtimeFilterForm(self.request.GET)
        return context
