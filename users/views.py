from django.utils import timezone
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm 
from django.contrib.auth import logout
from django.contrib.auth import  login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_GET
from django.contrib.auth.forms import AuthenticationForm
from cinemas.models import Cinema
from screeningrooms.models import ScreeningRoom
from showtimes.models import Showtime
from movies.models import Movie
from django.contrib.auth.models import User
from bookings.models import Booking
from django.core.paginator import Paginator



def is_staff(user):
    """Check if the user is a staff member or a superuser."""
    return user.is_staff or user.is_superuser

class AdminDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'users/admin_dashboard.html'

    def test_func(self):
        """Ensure the user passes the is_staff check before granting access."""
        return is_staff(self.request.user)

    def get_context_data(self, **kwargs):
        """Fetch and paginate all items for each admin dashboard section."""
        context = super().get_context_data(**kwargs)

        # Order and paginate the querysets for each section
        context['cinemas'] = self.paginate_queryset(Cinema.objects.all().order_by('id'), 'cinemas_page')
        context['screening_rooms'] = self.paginate_queryset(ScreeningRoom.objects.all().order_by('id'), 'screening_rooms_page')
        context['movies'] = self.paginate_queryset(Movie.objects.all().order_by('id'), 'movies_page')
        context['showtimes'] = self.paginate_queryset(Showtime.objects.all().order_by('showtime'), 'showtimes_page')
        context['users'] = self.paginate_queryset(User.objects.all().order_by('username'), 'users_page')
        context['bookings'] = self.paginate_queryset(Booking.objects.all().order_by('id'), 'bookings_page')

        return context

    def paginate_queryset(self, queryset, page_param):
        """Paginate the ordered queryset based on the given page parameter."""
        paginator = Paginator(queryset, 5)
        page_number = self.request.GET.get(page_param, 1)
        return paginator.get_page(page_number)
    
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) 
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully, now you can login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.info(request, f"You are now logged in as {user.username}.")
            return redirect('movie_list')
        else:
            messages.error(request, "Username or Password is incorrect.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
@require_GET
def logout_view(request):
    logout(request)
    messages.success(request, f'You  have been logged out!')
    return redirect('movie_list')

@login_required
def profile(request):
    # Fetch bookings, ensuring current bookings are for future showtimes
    current_bookings_query = Booking.objects.filter(
        user=request.user, 
        showtime__showtime__gte=timezone.now()
    ).select_related('showtime', 'showtime__movie', 'showtime__screening_room', 'showtime__screening_room__cinema').order_by('showtime__showtime')
    
    # Fetch past bookings for past showtimes
    past_bookings_query = Booking.objects.filter(
        user=request.user, 
        showtime__showtime__lt=timezone.now()
    ).select_related('showtime', 'showtime__movie', 'showtime__screening_room', 'showtime__screening_room__cinema').order_by('-showtime__showtime')

    # Paginate current bookings
    current_page_number = request.GET.get('current_page', 1)
    current_paginator = Paginator(current_bookings_query, 5)  # 5 bookings per page for example
    current_bookings = current_paginator.get_page(current_page_number)

    # Paginate past bookings
    past_page_number = request.GET.get('past_page', 1)
    past_paginator = Paginator(past_bookings_query, 5)  # Adjust the number as needed
    past_bookings = past_paginator.get_page(past_page_number)

    context = {
        'current_bookings': current_bookings,
        'past_bookings': past_bookings,
        'u_form': UserUpdateForm(instance=request.user),
        'p_form': ProfileUpdateForm(instance=request.user.profile),
    }

    return render(request, 'users/profile.html', context)

@login_required
@user_passes_test(is_staff)
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'The user has been updated.')
            return redirect('admin_dashboard')
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user': user
    }
    return render(request, 'users/edit_user.html', context)

@login_required
@user_passes_test(is_staff)
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'The user has been deleted.')
        return redirect('admin_dashboard')
    return render(request, 'users/delete_user.html', {'user': user})
