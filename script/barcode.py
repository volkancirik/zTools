#! /usr/bin/env python

import win32com.client
import os

os.system("C:/VBS/two.vbs")

#vbhost = win32com.client.Dispatch("ScriptControl")
#vbhost.language = "vbscript"
#vbhost.addcode("Function printLabel()\n Set Nice = CreateObject('NiceLabel5.Application') \n End Function\n")
#print vbhost.eval("printLabel()")