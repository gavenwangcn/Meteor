'''
Created on 2015

@author: 14020107
'''
# -*- coding: utf-8 -*-

import ConfigParser
import os

def getConfig(section, key):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/send.conf'
    config.read(path)
    return config.get(section, key)

if __name__ == '__main__':
    uri =getConfig("filter","uri")
    if not uri:
        print "have not uri"
    print uri