#! /usr/bin/env python

from sys import path

path.insert(0, '/home/dan/Projects/urwid') # FIXME: remove!

print path

from logger import LoggingCallLogger, DecorateAll
import logging

logging.basicConfig(filename='inquisition.log', level=logging.DEBUG)
logger = LoggingCallLogger(logging.getLogger())

cclogger = DecorateAll(logger.log_call)

import urwid

from nodes import DictionaryNode

class ObjectInspector(object):
    def __init__(self, root_node):
        self.treelistbox = urwid.TreeListBox(urwid.TreeWalker(root_node))
        self.treelistbox.offset_rows = 1

    def loop(self):
        return urwid.MainLoop(self.treelistbox)

if __name__ == '__main__':
    node = DictionaryNode('locals', locals())
    objins = ObjectInspector(node)
    loop = objins.loop()
    loop.run()
