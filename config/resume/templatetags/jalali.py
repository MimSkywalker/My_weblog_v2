import jdatetime
from django import template

register = template.Library()


JALALI_MONTHS = {
    1: 'فروردین',
    2: 'اردیبهشت',
    3: 'خرداد',
    4: 'تیر',
    5: 'مرداد',
    6: 'شهریور',
    7: 'مهر',
    8: 'آبان',
    9: 'آذر',
    10: 'دی',
    11: 'بهمن',
    12: 'اسفند',
}


def to_persian_digits(value):
    return str(value).translate(
        str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
    )


@register.filter
def jalali_year(value):
    if not value:
        return ''

    jalali = jdatetime.date.fromgregorian(date=value)

    return to_persian_digits(jalali.year)


@register.filter
def jalali_date(value):
    if not value:
        return ''

    jalali = jdatetime.date.fromgregorian(date=value)

    day = to_persian_digits(jalali.day)
    month = JALALI_MONTHS[jalali.month]
    year = to_persian_digits(jalali.year)

    return f'{day} {month} {year}'
