from django import template

register = template.Library()

@register.filter
def add_class(value, arg):
    """
    Custom filter to add a CSS class to form fields
    """
    return value.as_widget(attrs={'class': arg})
