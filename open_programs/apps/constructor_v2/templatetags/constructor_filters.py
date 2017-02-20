from django import template
register = template.Library()

from programs.models import Program


@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)


@register.filter
def percentage(value):
    return '{0:.2%}'.format(value)


@register.filter
def to_list_ui(queryset):
    return str([str(item) for item in queryset])


@register.filter
def to_list(queryset):
    return [str(item) for item in queryset]
