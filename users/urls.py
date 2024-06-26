from django.urls import path
from .views import (
    register, login, logout_view, profile,
    edit_user, delete_user, AdminDashboardView, change_user_staff_status,
    CustomPasswordResetView, CustomPasswordResetConfirmView, CustomPasswordResetDoneView

)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/',  login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('admin/change_staff_status/<int:user_id>/', change_user_staff_status, name='change_user_staff_status'),
    path('password-reset/', CustomPasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
]
