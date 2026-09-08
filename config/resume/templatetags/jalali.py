import jdatetime
from django import template

register = template.Library()


@register.filter
def jalali_year(value):
    if not value:
        return ''

    return jdatetime.date.fromgregorian(date=value).year