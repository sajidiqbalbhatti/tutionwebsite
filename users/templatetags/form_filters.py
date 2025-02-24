from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """Add a CSS class to form fields dynamically."""
    existing_classes = field.field.widget.attrs.get('class', '')
    classes = existing_classes + ' ' + css_class
    if field.errors:  # Add 'is-invalid' class if there are errors
        classes += ' is-invalid'
    return field.as_widget(attrs={'class': classes.strip()})
