#! /usr/bin/env python

from sys import path

path.insert(0, '/home/dan/Projects/urwid') # FIXME: remove!

from logger import LoggingCallLogger, DecorateAll
import logging

logging.basicConfig(filename='inquisition.log', level=logging.DEBUG)
logger = LoggingCallLogger(logging.getLogger())

cclogger = DecorateAll(logger.log_call)

import urwid

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

def inspect_object(obj, name='Root Object'):
    from nodes import ObjectNode
    node = ObjectNode(name, obj)
    ObjectInspector(node).loop().run()

def inspect_dictionary(dict, name="Root Dictionary"):
    from nodes import DictionaryNode
    node = DictionaryNode(name, dict)
    ObjectInspector(node).loop().run()

if __name__ == '__main__':
    inspect_dictionary(locals(), 'locals')
