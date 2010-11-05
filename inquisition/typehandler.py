import types
import numbers
import inspect
import collections

class RedundantDict(collections.MutableMapping):
    def __init__(self, mapping=None, priorities=None):
        if mapping:
            self._storage = dict(mapping.iteritems())
        else:
            self._storage = []

        if priorities:
            self._priorities = dict(priorities.iteritems())
        else:
            self._priorities = {}

    def set_priority_list(self, key, priorities):
        self._priorities[key] = priorities

    def set_priority_list_merge(self, priorities_list):
        pass
    
    def __getitem__(self, key):
        try:
            priorities = self._priorities[key]
        except KeyError, e:
            priorities = [key]

        for key in priorities:
            try:
                return self._storage[key]
            except KeyError, e:
                continue
        raise KeyError() # TODO: message

    def __setitem__(self, key, value):
        self._storage[key] = value

# This module is mostly redundant
# however it smooths over some things
# so client code is (hopefully)
# cleaner.

MethodWrapperType = type([].__str__)

class TypeHandler(object):
    def is_function_like(self, x):
        if inspect.isroutine(object):
            return True
        elif isinstance(x, MethodWrapperType):
            return True
        else:
            return False

    def is_stringlike(self, x):
        if isinstance(x, str):
            return True
        elif isinstance(x, unicode):
            return True
        else:
            return False

    def is_numeric(self, x):
        return isinstance(x, numbers.Number)

    def is_integral(self, x):
        return isinstance(x, numbers.Integral)

    def is_primitive(self, x):
        if self.is_numeric(x):
            return True
        elif self.is_stringlike(x):
            return True
