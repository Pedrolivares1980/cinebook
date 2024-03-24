# myapp/templatetags/rating_stars.py
from django import template

register = template.Library()

@register.filter(name='stars_range')
def stars_range(value):
    """
    Splits the rating into full stars, half stars, and empty stars.
    Returns a dictionary with the counts of each.
    """
    full_stars = int(value)
    half_star = 1 if value - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    return {
        'full_stars': range(full_stars),
        'half_star': range(half_star),
        'empty_stars': range(empty_stars),
    }
