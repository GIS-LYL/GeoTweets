# -*- coding: utf-8 -*-
'''import sys

print 'Name:' + sys.argv[0]
print 'Argument:'
for argu in sys.argv:
    print argu'''
    
class A:
    def __init__(self):
        print hasattr(self, 'x')
        self.x = 1
        print hasattr(self, 'x')
        
a = A()