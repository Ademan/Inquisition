import urwid

from urwid.canvas import TextCanvas

from __main__ import logger

log_call = logger.log_call

class TreeLabelWidget(urwid.Text):
    def __init__(self, tree_widget, tree_node):
        urwid.Text.__init__(self, '') # XXX: necessary?
        self.tree_widget = tree_widget
        self.tree_node = tree_node

    @log_call
    def render(self, size, focus=False):
        namestr = self.tree_node.render_name()
        objectstr = self.tree_node.render_value()

        spare_room = size[0] - len(namestr) - len(objectstr)
        
        if spare_room > 0:
            text = (' ' * spare_room).join([namestr, objectstr])
        elif size[0] - len(namestr) > 4:
            spare_room = size[0] - len(namestr) - 3
            text = (' ' * spare_room).join([namestr, "..."])
        else:
            spare_room = size[0] - len(namestr)
            text = namestr + (' ') * spare_room
        return TextCanvas([text], maxcol=size[0])

class ObjectWidget(urwid.TreeWidget):
    def __init__(self, node):
        super(ObjectWidget, self).__init__(node)
        #self.expanded = True
        self.is_leaf = False
    def load_inner_widget(self):
        return TreeLabelWidget(self, self.get_node())

    def selectable(self): return True
