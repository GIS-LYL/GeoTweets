#!/usr/bin/env python
#-*-coding = utf-8-*-
import mechanize
import sys

br = mechanize.Browser()
response = br.open(sys.argv[1])
for form in br.forms():
    print "name:[%r] id:[%r] action:[%s]" %(form.name, form.attrs.get('id'), form.action)
    print "Controls: "
    for control in form.controls:
        print '    ', control.type, control.name, repr(control.value)
    print(" ")