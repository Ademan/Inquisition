import itertools
import urwid

class ViewedObject(urwid.ParentNode):
    def __init__(self, name, object, parent=None, depth=0, views={}):
        super(ViewedObject, self).__init__(name, key=name,
                                           parent=parent, depth=depth)
        self.name = name
        self.object = object
        self.views = {view.name, view}
        self.view_iter = itertools.cycle(self.views.keys())
        self.current_view = self.view_iter.next()

    def next_view(self):
        self.current_view = self.view_iter.next()
        self.get_child_keys(reload=True)

    def load_widget(self):
        self.current_view.load_widget()

    def load_child_keys(self):
        return self.views.keys()

class ObjectView(object):
    def __init__(self, node):
        self.node = node

    def load_widget(self):
        return TreeLabelWidget(self, self.get_node())

    def load_child_widget(self): pass

class ObjectViewNode(urwid.ParentNode):
    def __init__(self, name, object, parent=None, depth=0, view=None):
        super(ObjectViewNode, self).__init__(name, key=name,
                                             parent=parent, depth=depth)
        self.name = name
        self.object = object
        self.view = view

    def load_widget(self):
        self.view.load_child_widget()

class ObjectWidget(urwid.TreeWidget):
    def __init__(self, node):
        super(ObjectWidget, self).__init__(node)
        self.expanded = False

    @property
    def is_leaf(self):
        try:
            return not bool(self.get_node().get_child_keys())
        except AttributeError, e:
            return True

    @is_leaf.setter
    def is_leaf(self, value): pass

    def load_inner_widget(self):
        return TreeLabelWidget(self, self.get_node())

    def selectable(self): return True
