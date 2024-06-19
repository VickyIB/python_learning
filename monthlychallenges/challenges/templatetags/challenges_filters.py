# challenges/templatetags/challenges_filters.py
from django import template

register = template.Library()

@register.filter(name='capitalize')
def capitalize(value):
    return value.capitalize()
