import urwid

from __main__ import logger
log_call = logger.log_call

def object_node_type(object):
        if inspect.isroutine(object):
            return FunctionNode
        try:
            return _primitives[type(object)]
        except KeyError, e:
            return FilteredObjectNode

class ObjectNode(urwid.ParentNode): # FIXME: TreeNode
    def __init__(self, name, object, parent=None, depth=0):
        super(ObjectNode, self).__init__(name, key=name,
                                parent=parent, depth=depth)
        self.name = name
        self.object = object

    def create_child_node(self, name, object):
        NodeType = object_node_type(object)
        return NodeType(name, object, parent=self, depth=self.get_depth()+1)

    def render_child_name(self, name):
        return str(name)

    def render_name(self):
        return self.get_parent().render_child_name(self.name)

    def render_value(self):
        return str(self.object)

    def has_children(self): return True

    @log_call
    def load_child_node(self, key):
        object = getattr(self.object, key)
        return self.create_child_node(key, object)

    @log_call
    def load_child_keys(self):
        return dir(self.object)

    def load_widget(self):
        import widgets
        return widgets.ObjectWidget(self)

    get_child_node = urwid.ParentNode.get_child_node

class DictionaryNode(ObjectNode):
    def render_name(self):
        return repr(self.name)

    def load_child_node(self, key):
        object = self.object[key]
        return self.create_child_node(key, object)

    @log_call
    def load_child_keys(self):
        return self.object.keys()

class ObjectFilterNode(ObjectNode):
    filter_name = 'Default Filter'
    def __init__(self, parent):
        super(ObjectFilterNode, self).__init__(self.filter_name, parent.object,
                                               parent=parent, depth=parent.get_depth()+1)
        self.parent = parent
        self.keys = []

    def append(self, value):
        self.keys.append(value)

    @log_call
    def load_child_keys(self):
        return self.keys if self.keys else None

    def load_child_node(self, key):
        object = getattr(self.parent.object, key)
        return self.create_child_node(key, object)

    def key_filter(self, key): return True

class ObjectOperatorsNode(ObjectFilterNode):
    filter_name = "Operators"
    # TODO: finish operator list
    comparison_operators = ['__lt__', '__gt__',
                            '__eq__', '__cmp__', '__ne__',
                            '__le__', '__ge__']
    boolean_operators = ['__not__', '__and__', '__or__', '__bool__']
    math_operators = ['__add__', '__sub__',
                      '__radd__', '__rsub__',
                      '__iadd__', '__isub__',
                      '__mul__', '__div__',
                      '__rmul__', '__rdiv__',
                      '__imul__', '__idiv__',
                      '__pow__',
                      '__pos__', '__neg__',]
    binary_operators = ['__inv__', '__lshift__', '__rshift__']
    sequence_operators = ['__concat__', '__contains__',
                          '__getitem__', '__getslice__',
                          '__setitem__', '__setslice__',
                          '__delitem__', '__delslice__',]
    basic_operators = ['__int__', '__str__', '__unicode__', '__repr__']

    operators = comparison_operators + boolean_operators + math_operators + binary_operators + basic_operators

    def key_filter(self, key):
        return key in self.operators

class SpecialObjectNode(ObjectFilterNode):
    filter_name = "Special Attributes"
    from re import compile
    test = compile('__\w+__')

    def key_filter(self, key):
        return bool(self.test.match(key))

class FilteredObjectNode(ObjectNode):
    filter_nodes = [ObjectOperatorsNode, SpecialObjectNode, ObjectFilterNode]
    def __init__(self, name, object, parent=None, depth=0):
        super(FilteredObjectNode, self).__init__(name, object,
                                                 parent=parent, depth=depth)
        self.name = name
        self.object = object
        self.children = []
        self.filters = dict([(filter.filter_name, filter(self)) for filter in self.filter_nodes])

    @log_call
    def load_child_keys(self):
        for key in dir(self.object):
            for filter in self.filters.itervalues():
                if filter.key_filter(key):
                    filter.append(key)
                    break
        return self.filters.keys()

    def load_child_node(self, key):
        return self.filters[key]

class DataNode(ObjectNode):
    def has_children(self): return False

    def load_child_node(self, key):
        return None

    @log_call
    def load_child_keys(self):
        return None

class ReprNode(DataNode):
    def __init__(self, name, object, parent=None, depth=0):
        super(DataNode, self).__init__(name, object, parent=parent, depth=depth)
        self.name = name
        self.object = object

class SourceWidget(urwid.TreeWidget):
    def load_inner_widget(self):
        object = self.get_node().object
        return urwid.Text(inspect.getsource(object))

class SourceNode(DataNode):
    def load_widget(self):
        return SourceWidget(self)

class FunctionNode(ObjectNode):
    def render_value(self):
        reprstr = repr(self.object)
        try:
            f = self.object
            argspec = inspect.formatargspec(*inspect.getargspec(f))
            return '%s%s' % (self.object.__name__, argspec)
        except AttributeError, e:
            return reprstr
        except TypeError, e:
            return reprstr

    @log_call
    def load_child_keys(self):
        keys = ['repr']

        try:
            inspect.getsource(self.object)
            keys.append('source')
        except TypeError, e: pass
        except IOError, e: pass

        return keys

    def load_child_node(self, key):
        if key == 'repr':
            return ReprNode('repr', self.object,
                            parent=self, depth=self.get_depth()+1)
        elif key == 'source':
            return SourceNode('source', self.object,
                              parent=self, depth=self.get_depth()+1)

import types
import inspect

MethodWrapperType = type([].__str__)

_primitives = {int: DataNode,
               long: DataNode,

               str: DataNode,
               unicode: DataNode,

               float: DataNode,
               complex: DataNode,

               bool: DataNode,
               types.NoneType: DataNode,
               MethodWrapperType: FunctionNode,
               }

