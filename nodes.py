import urwid

class ObjectNode(urwid.ParentNode): # FIXME: TreeNode
    def __init__(self, name, object, parent=None, depth=0):
        super(ObjectNode, self).__init__(name, key=name,
                                parent=parent, depth=depth)
        self.name = name
        self.object = object

    def create_child_node(self, name, object):
        try:
            DataNodeType= _primitives[type(object)]
            return DataNodeType(name, object,
                            parent=self, depth=self.get_depth()+1)
        except KeyError, e:
            return ObjectNode(name, object,
                              parent=self, depth=self.get_depth()+1)

    def render_name(self):
        return str(self.name)

    def render_value(self):
        return str(self.object)

    def has_children(self): return True

    def load_child_node(self, key):
        object = getattr(self.object, key)
        return self.create_child_node(key, object)

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

    def load_child_keys(self):
        return self.object.keys()

class ObjectFilterNode(ObjectNode):
    def __init__(self, parent):
        ObjectNode.__init__(self, parent)
        self.parent = parent
        self.keys = []

    def append(self, value):
        self.keys.append(self)

    def load_child_keys(self):
        return self.keys

    def filter_key(self, key): return True

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

    operators = comparison_operators + boolean_operators + math_operators + binary_operators

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
    def __init__(self, name, object):
        self.object = object
        self.children = []
        self.filters = [filter(self) for filter in self.filter_nodes]

    def load_child_keys(self):
        for key in dir(self.object):
            for filter in self.filters:
                if filter.key_filter(key):
                    filter.append(key)

class DataNode(ObjectNode):
    def has_children(self): return False

    def load_child_node(self, key):
        return None

    def load_child_keys(self):
        return None

_primitives = {int: DataNode,
               str: DataNode,
               float: DataNode,
               }

