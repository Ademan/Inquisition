import types
import inspect

import urwid
from urwid.canvas import TextCanvas

MethodWrapperType = type([].__str__)

_primitive_list = [int, long, 
                   float, complex,
                   bool,
                   types.NoneType,
                   str, unicode]
                   
_primitives = dict([(t, 'primitive') for t in _primitive_list])

def attr_for_type(t):
    if inspect.isroutine(t):
        return 'method'
    try:
        return _primitives[t]
    except KeyError, e:
        return 'object'

class TreeLabelWidget(urwid.Text):
    def __init__(self, tree_widget, tree_node):
        urwid.Text.__init__(self, '') # XXX: necessary?
        self.tree_widget = tree_widget
        self.tree_node = tree_node

    def render_name(self):
        return str(self.tree_node.name)

    def render_object(self):
        return repr(self.tree_node.object)

    def render(self, size, focus=False):
        namestr = self.render_name()
        objectstr = self.render_object()
        nodeattr = attr_for_type(type(self.tree_node.object))

        spare_room = size[0] - len(namestr) - len(objectstr)
        
        if spare_room > 0:
            filler = ' ' * spare_room
            attributes = [('name', len(namestr)),
                          (None, spare_room),
                          (nodeattr, len(objectstr))]
            text = ''.join([namestr, filler, objectstr])
        elif size[0] - len(namestr) > 4:
            spare_room = size[0] - len(namestr) - 3
            filler = ' ' * spare_room
            objectstr = "..."
            attributes = [('name', len(namestr)),
                          (None, spare_room),
                          (nodeattr, 3)]
            text = ''.join([namestr, filler, objectstr])
        else:
            spare_room = size[0] - len(namestr)
            filler = ' ' * spare_room
            attributes = [('name', len(namestr)),
                          (None, spare_room)]
            text = ''.join([namestr, filler, objectstr])

        return TextCanvas([text], [attributes], maxcol=size[0])

class DictTreeLabelWidget(TreeLabelWidget):
    def render_name(self):
        return repr(self.tree_node.name)

class ObjectWidget(urwid.TreeWidget):
    def __init__(self, node):
        super(ObjectWidget, self).__init__(node)
        self.expanded = False

    @property
    def is_leaf(self):
        return not bool(self.get_node().get_child_keys())

    @is_leaf.setter
    def is_leaf(self, value): pass

    def load_inner_widget(self):
        return TreeLabelWidget(self, self.get_node())

    def selectable(self): return True
