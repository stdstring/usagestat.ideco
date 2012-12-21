from __future__ import unicode_literals

class StandardKeyTransformer(object):

    # spec: str, str, State -> str
    def __call__(self, key, value, state):
        # value is unused here
        if state.state_id is None:
            return key
        else:
            return '{category:s}.{key:s}'.format(category=state.state_id, key=key)

__author__ = 'andrey.ushakov'
