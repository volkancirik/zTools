import os
from openpyxl.workbook import Workbook
from openpyxl.reader.excel import load_workbook
from xlrd import open_workbook

from django import template
from settings import MEDIA_ROOT

register = template.Library()

@register.filter
def filename(value):

    return os.path.basename(value.file.name)

@register.filter
def lineCount(value):

    try:
        wb = load_workbook(filename = r'%s'%(value.file.name))
        return len(wb.worksheets[0].row_dimensions)
    except:
        pass

    try:
        book = open_workbook(value.file.name,encoding_override='utf-8')
        sheet = book.sheet_by_index(0)
        return sheet.nrows
    except:
        pass

    return 0