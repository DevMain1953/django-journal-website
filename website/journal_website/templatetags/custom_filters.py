from django import template
from django.utils.functional import SimpleLazyObject
from django.utils.safestring import SafeString


register = template.Library()


@register.filter(name="in_group")
def in_group(user: SimpleLazyObject, group_name: SafeString) -> bool:
    return user.groups.filter(name=group_name).exists()