# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 13:25:11 2020

@author: vz237
"""

from time import sleep

with open('hi.txt','a') as f:
    for i in range(10):
        f.write('{}\n'.format(i))
        sleep(0.5)