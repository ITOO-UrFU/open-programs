from django import template
register = template.Library()


@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)


@register.filter
def percentage(value):
    return '{0:.2%}'.format(value)