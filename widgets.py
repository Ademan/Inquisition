import urwid

from urwid.canvas import TextCanvas

class TreeLabelWidget(urwid.Text):
    def __init__(self, tree_widget, tree_node):
        urwid.Text.__init__(self, '') # XXX: necessary?
        self.tree_widget = tree_widget
        self.tree_node = tree_node

    def render(self, size, focus=False):
        namestr = self.tree_node.render_name()
        objectstr = self.tree_node.render_value()
        nodeattr = self.tree_node.attribute_name()

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

class ObjectWidget(urwid.TreeWidget):
    def __init__(self, node):
        super(ObjectWidget, self).__init__(node)
        self.expanded = False
    def load_inner_widget(self):
        return TreeLabelWidget(self, self.get_node())

    def selectable(self): return True
