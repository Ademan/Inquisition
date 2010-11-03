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
    palette = [('body', 'default', 'black'),
               ('name', 'dark green', 'black'),
               ('object', 'dark blue', 'black'),
               ('primitive', 'dark red', 'black'),
               ('method', 'yellow', 'black'),
               ]

    def __init__(self, root_node):
        self.treelistbox = urwid.TreeListBox(urwid.TreeWalker(root_node))
        self.treelistbox.offset_rows = 1

    def unhandled_keys(self, key):
        try:
            if key in 'qQ':
                raise urwid.ExitMainLoop
        except TypeError, e: pass

    def loop(self):
        self.loop = urwid.MainLoop(urwid.AttrWrap(self.treelistbox, 'body'),
                                   self.palette, unhandled_input=self.unhandled_keys)
        return self.loop

if __name__ == '__main__':
    node = DictionaryNode('locals', locals())
    objins = ObjectInspector(node)
    loop = objins.loop()
    loop.run()
