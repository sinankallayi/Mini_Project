# yourapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def stars(rating):
    return '★' * rating + '☆' * (5 - rating)
