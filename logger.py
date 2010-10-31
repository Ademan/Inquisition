from functools import wraps

class CallLogger(object):
    def __init__(self):
        self.indentation = 0
    
    def argstrs(self, args, kwargs):
        argstr = ', '.join([repr(arg) for arg in args])
        kwargstr = ', '.join(["%s=%s" % (k, v) for k, v in kwargs.iteritems()])

        if argstr and kwargstr:
            return ', '.join([argstr, kwargstr])
        elif argstr:
            return argstr
        else:
            return kwargstr

    def log(self, logstr, depth=0):
        print ' ' * depth, logstr

    def log_call(self, f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            argstr = self.argstrs(args, kwargs)
            self.log("%s(%s)" % (f.__name__, argstr), depth=self.indentation)
            self.indentation += 1
            result = f(*args, **kwargs)
            self.indentation -= 1
            self.log("%s(%s)->%r" % (f.__name__, argstr, result), depth=self.indentation)
            return result
        return wrapped

class LoggingCallLogger(CallLogger):
    def __init__(self, logger):
        self.logger = logger
        self.indentation = 0

    def log(self, logstr, depth=0):
        self.logger.debug(' ' * depth + logstr)

from types import MethodType

class DecorateAll(object):
    def __init__(self, decorator):
        self.decorator = decorator
    def __call__(self, cls):
        for attrname in dir(cls):
            attr = getattr(cls, attrname)
            if isinstance(attr, MethodType):
                setattr(cls, attrname, self.decorator(attr))
        return cls
