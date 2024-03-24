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
from django.contrib.auth import get_user_model




def is_staff(user):
    """Check if the user is a staff member or a superuser."""
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_staff)
def change_user_staff_status(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_id)
    user.is_staff = not user.is_staff
    user.save()
    messages.success(request, f"Updated {user.username}'s staff status.")
    return redirect('admin_dashboard')

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
    
# User registration view
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
    # Updating user and profile information
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # Fetch bookings, ensuring current bookings are for future showtimes
    current_bookings_query = Booking.objects.filter(
        user=request.user, 
        showtime__showtime__gte=timezone.now()
    ).select_related('showtime', 'showtime__movie', 'showtime__screening_room', 'showtime__screening_room__cinema').order_by('showtime__showtime')
    

    # Paginate current bookings
    current_page_number = request.GET.get('current_page', 1)
    current_paginator = Paginator(current_bookings_query, 5) 
    current_bookings = current_paginator.get_page(current_page_number)


    context = {
        'current_bookings': current_bookings,
        'u_form': UserUpdateForm(instance=request.user),
        'p_form': ProfileUpdateForm(instance=request.user.profile),
    }

    return render(request, 'users/profile.html', context)

@login_required
def edit_user(request, user_id=None):
    """
    Edit a user's profile. If user_id is provided, it's assumed that an admin is editing
    another user's profile. Otherwise, users are editing their own profile.
    """
    User = get_user_model()

    # Determine if the current user is editing their own profile or an admin is editing another's profile
    is_admin_editing = user_id is not None and (request.user.is_staff or request.user.is_superuser)
    
    # Fetch the user to be edited. If user_id is not provided, default to the current user.
    user_to_edit = get_object_or_404(User, id=user_id) if user_id else request.user

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user_to_edit)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_to_edit.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'The profile has been updated successfully!')
            
            # Redirect based on who is editing the profile
            if is_admin_editing:
                return redirect('admin_dashboard')
            else:
                return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=user_to_edit)
        p_form = ProfileUpdateForm(instance=user_to_edit.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'is_admin_editing': is_admin_editing,
        'user_to_edit': user_to_edit,
    }

    return render(request, 'users/edit_user.html', context)

@login_required
def delete_user(request, user_id=None):
    user_to_delete = get_object_or_404(User, id=user_id)
    if request.user == user_to_delete or request.user.is_staff:
        if request.method == "POST":
            user_to_delete.delete()
            messages.success(request, 'The user account has been successfully deleted.')
            return redirect('movie_list') if request.user == user_to_delete else redirect('admin_dashboard')
        return render(request, 'users/delete_user.html', {'user': user_to_delete})
    else:
        messages.error(request, 'You do not have permission to delete this user.')
        return redirect('movie_list')
