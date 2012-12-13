from __future__ import unicode_literals

class DaemonRunner(object):

    def __init__(self, run_func):
        self._run_func = run_func

    def start(self):
        pass

    def stop(self):
        pass

    def restart(self):
        pass

    def _daemonize(self):
        pass

    def _remove_pidfile(self):
        pass

__author__ = 'andrey.ushakov'