from __future__ import unicode_literals

class StandardKeyTransformer(object):

    # spec: str, State -> str
    def __call__(self, key, state):
        return '%(category)s.%(key)s' % {'category': state.state_id, 'key':key}

__author__ = 'andrey.ushakov'
