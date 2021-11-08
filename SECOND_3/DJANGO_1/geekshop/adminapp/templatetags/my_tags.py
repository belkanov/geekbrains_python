from django import template

register = template.Library()


@register.filter(name='my_title')
def my_title(string):
    return string.upper()
