def is_staff(user):
    """Check if the user is a staff member or a superuser."""
    return user.is_staff or user.is_superuser