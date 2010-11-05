#! /usr/bin/env python

from sys import path

path.insert(0, '/home/dan/Projects/urwid') # FIXME: remove!

from logger import LoggingCallLogger, DecorateAll
import logging

logging.basicConfig(filename='inquisition.log', level=logging.DEBUG)
logger = LoggingCallLogger(logging.getLogger())

cclogger = DecorateAll(logger.log_call)

if __name__ == '__main__':
    from inquisition import inspect_dictionary
    inspect_dictionary(locals(), 'locals')
