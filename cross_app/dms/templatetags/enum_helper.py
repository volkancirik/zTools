import os
from django.utils.safestring import mark_safe
from django import template
register = template.Library()

@register.simple_tag()
def enum2option(enumClass):
    tag = ""
    for e in enumClass:
        tag += ("<option value='%s'>%s</value>"%(str(e[0]),str(e[1])))

    return mark_safe(tag)

@register.filter()
def getEnumName(val):
    return str(val[1])