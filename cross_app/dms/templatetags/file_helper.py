import os
from xlrd import open_workbook

from django import template
register = template.Library()

@register.filter
def filename(value):
    
    return os.path.basename(value.file.name)

@register.filter
def lineCount(value):
    return 0