from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from .views import (
    register, login, logout_view, profile,
    edit_user, delete_user, AdminDashboardView
)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/',  login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('edit_user/<int:pk>/', edit_user, name='edit_user'),
    path('delete_user/<int:pk>/', delete_user, name='delete_user'),
]
