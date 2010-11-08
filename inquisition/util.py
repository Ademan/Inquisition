def render_function(f):
    reprstr = repr(f)
    try:
        argspec = inspect.formatargspec(*inspect.getargspec(f))
        return '%s%s' % (self.object.__name__, argspec)
    except AttributeError, e:
        return reprstr
    except TypeError, e:
        return reprstr

def split_render(left, right, left_attr='', right_attr=''):
    namestr = left
    objectstr = right
    spare_room = size[0] - len(namestr) - len(objectstr)
    
    if spare_room > 0:
        filler = ' ' * spare_room
        attributes = [(left_attr, len(namestr)),
                      (None, spare_room),
                      (right_attr, len(objectstr))]
        text = ''.join([namestr, filler, objectstr])
    elif size[0] - len(namestr) > 4:
        spare_room = size[0] - len(namestr) - 3
        filler = ' ' * spare_room
        objectstr = "..."
        attributes = [(left_attr, len(namestr)),
                      (None, spare_room),
                      (right_attr, 3)]
        text = ''.join([namestr, filler, objectstr])
    else:
        spare_room = size[0] - len(namestr)
        filler = ' ' * spare_room
        attributes = [(left_attr, len(namestr)),
                      (None, spare_room)]
        text = ''.join([namestr, filler, objectstr])

    return TextCanvas([text], [attributes], maxcol=size[0])
