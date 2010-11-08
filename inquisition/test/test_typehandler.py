import py

from inquisition.type_handler import RedundantDict

class TestRedundantDict(object):
    def test_update_roots(self):
        x = RedundantDict()
        x.set_path('foo', ['foo'])
        x.update_roots('foo', ['bar', 'baz'])
        assert x.get_path('foo') == ['foo', 'bar', 'baz']

        x.set_path('spam', ['spam', 'eggs'])
        x.update_roots('eggs', ['bar', 'baz'])
        assert x.get_path('spam') == ['spam', 'eggs', 'bar', 'baz']

    def test_normalize_paths(self):
        x = RedundantDict()
        x.set_path('foo', ['foo', 'bar', 'baz'])
        x.set_path('bar', ['bar'])
        x.set_path('spam', ['spam', 'bar'])
        x.set_path('eggs', ['eggs', 'baz'])
        x.normalize_paths()

        assert x.get_path('foo') == ['foo', 'bar', 'baz']
        assert x.get_path('bar') == ['bar', 'baz']
        assert x.get_path('spam') == ['spam', 'bar', 'baz']
        assert x.get_path('eggs') == ['eggs', 'baz']

