from django import template

register = template.Library()


@register.filter
def hourly_to_monthly(price):
    if not price:
        return ''
    return '${:,.2f}'.format(price * 730)


@register.filter
def price(price):
    if not price:
        return ''
    if price >= 100:
        return '${:,.2f}'.format(price)
    else:
        return '${:,.3f}'.format(price)
