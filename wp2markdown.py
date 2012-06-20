#-*- coding: utf-8 -*-

""" wp documents to markdown file      """
""" author: xiaomo(wxm4ever@gmail.com) """

import sys,os,re

from datetime import datetime
from xml.sax import handler, parseString


def log(msg): print msg

class WPDocumentHandler(handler.ContentHandler):
    def __init__(self):
        self.items_count = 0
        self.in_item = False
        self.items = {}
        self.value = ''

    def startDocument(self):
        log("=====================================")
        log("*** Document start...")

    def endDocument(self):
        log("=====================================")
        log("*** Document end...")
        log("*** Items Count: %d" % self.items_count)

    def startElement(self, name, attr):
        if name == 'item':
            self.items_count += 1
            self.in_item = True

    def endElement(self, name):
        if name == 'item':
            self.in_item = False
            # write item to file
            if self.items['status'] == 'publish':
                # deal with the date string
                date_str = self.items['date'].split('+')[0]
                date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S ')
                self.items['date'] = datetime.strftime(date, '%Y-%m-%d %H:%M')

                filename = os.path.normpath(datetime.strftime(date, '%Y-%m-%d-') + '%s.markdown' % self.items['title'])
                filename = re.subn(r'/', r'-', filename)[0]
                with open('tmp/'+filename, 'w') as f:
                    f.write("---\nlayout: post\n")
                    f.write("title: \"%s\"\n" % self.items['title'].encode('utf-8'))
                    f.write("date: %s\n" % self.items['date'])
                    f.write("comments: true\n")
                    f.write("categories: %s\n" % self.items['category'].encode('utf-8'))
                    f.write("---\n")
                    f.write("\n%s\n" % self.items['content'].encode('utf-8'))

        if self.in_item == True:
            if name == 'title':
                self.items['title'] = self.value.strip()
                self.items['title'] = re.subn(r' ', r'_', self.items['title'])[0]
            elif name == 'pubDate':
                self.items['date'] = self.value.strip()
            elif name == 'content:encoded':
                self.items['content'] = self.value.strip()
            elif name == 'wp:status':
                self.items['status'] = self.value.strip()
            elif name == 'category':
                self.items['category'] = self.value.strip()

        self.value = ''

    def characters(self, content):
        self.value += content

if __name__ == '__main__':
    xml_file = sys.argv[1]
    try:
        with open(xml_file) as f:
            parseString(f.read(), WPDocumentHandler())
    except Exception as e:
        print str(e)
