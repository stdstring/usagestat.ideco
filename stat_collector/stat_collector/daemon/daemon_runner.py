from __future__ import unicode_literals
import atexit
import os
import sys
import signal
from stat_collector.daemon.daemon import daemonize

class DaemonRunner(object):

    def __init__(self, run_func, logger, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self._run_func = run_func
        self._logger = logger
        self._pidfile = pidfile
        self._stdin=stdin
        self._stdout=stdout
        self._stderr=stderr

    def start(self):
        # Start the daemon
        self._logger.info('start() enter')
        # Check for a pidfile to see if the daemon already runs
        pid = self._read_pidfile()
        if pid:
            message = 'error in start(): pidfile {0:s} already exist. Daemon already running?'.format(self._pidfile)
            self._logger.exception(message)
            sys.stderr.write(message + '\n')
            sys.exit(1)
        # Start the daemon
        daemonize(self._logger, self._stdin, self._stdout, self._stdout)
        # prepare pidfile
        atexit.register(self._remove_pidfile)
        self._write_pidfile()
        self._logger.info('start() exit. now run user-defined functionality')
        # run main functionality
        self._run_func()

    def stop(self):
        # Stop the daemon
        self._logger.info('stop() enter')
        # Get the pid from the pidfile
        pid = self._read_pidfile()
        if not pid:
            message = 'error in stop(): pidfile {0:s} does not exist. Daemon not running?'.format(self._pidfile)
            self._logger.exception(message)
            sys.stderr.write(message + '\n')
            return # not an error in a restart
        # Try killing the daemon process
        self._terminate_daemon_proc(pid)
        self._logger.info('stop() exit')

    def restart(self):
        self.stop()
        self.start()

    def _read_pidfile(self):
        pid = None
        pf = open(self._pidfile, 'r')
        try:
            pid = int(pf.read().strip())
        except IOError:
            pass
        finally:
            pf.close()
        return pid

    def _write_pidfile(self):
        pid = os.getpid()
        with open(self._pidfile,'w') as pf:
            pf.write('{0!s}\n'.format(pid))


    def _remove_pidfile(self):
        if os.path.exists(self._pidfile):
            os.remove(self._pidfile)

    def _terminate_daemon_proc(self, pid):
        os.kill(pid, signal.SIGTERM)
        self._remove_pidfile()

__author__ = 'andrey.ushakov'