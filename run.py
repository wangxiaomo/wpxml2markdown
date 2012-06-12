#-*- coding: utf-8 -*-

import os,sys,re
from xml.sax import parseString
from wpxml2markdown import WPDocumentHandler

path = sys.argv[1]
if not os.path.isdir(path):
    raise Exception("*** %s not a directory!" % path)

files = os.listdir(path)
for filename in files:
    real_path = os.path.join(path, filename)
    if re.match('.*xml$', real_path) and os.path.isfile(real_path):
        print "*** FILE: %s" % real_path
        try:
            with open(real_path) as f:
                parseString(f.read(), WPDocumentHandler())
        except Exception as e:
            print "*** Exception: %s" % str(e)
