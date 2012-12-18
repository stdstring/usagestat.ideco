from __future__ import unicode_literals
import os
import sys
import signal
import resource

def daemonize(logger, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    # do the UNIX double-fork magic, see Stevens' "Advanced Programming in the UNIX Environment" for details
    logger.info('daemonize(stdin={0:s}, stdout={1:s}, stderr={2:s}) enter'.format(stdin, stdout, stderr))
    (soft_flimit, hard_flimit) = resource.getrlimit(resource.RLIMIT_NOFILE)
    _fork(1, logger)
    # decouple from parent environment
    os.chdir("/")
    os.setsid()
    os.umask(0)
    # ignore SIGHUP
    _ignore_signal(signal.SIGHUP, logger)
    # do second fork
    _fork(2, logger)
    sys.stdout.flush()
    sys.stderr.flush()
    # close all file descriptors
    os.closerange(0, hard_flimit)
    # redirect standard file descriptors
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
    logger.info('daemonize(stdin={0:s}, stdout={1:s}, stderr={2:s}) exit'.format(stdin, stdout, stderr))

def _fork(fork_number, logger):
    logger.info('_fork #{0:d} enter'.format(fork_number))
    try:
        pid = os.fork()
        if pid > 0:
            # exit parent
            sys.exit(0)
    except OSError as e:
        logger.exception('_fork #{0:d} failed: {1:d} ({2:s})'.format(fork_number, e.errno, e.strerror))
        sys.stderr.write('fork #{0:d} failed: {1:d} ({2:s})\n'.format(fork_number, e.errno, e.strerror))
        sys.exit(1)
    logger.info('_fork #{0:d} exit'.format(fork_number))

def _ignore_signal(signo, logger):
    logger.info('_ignore_signal({0:d}) enter'.format(signo))
    try:
        signal.signal(signo, signal.SIG_IGN)
    except OSError as e:
        logger.exception('_ignore_signal({0:d}) failed: {1:d} ({2:s})'.format(signo, e.errno, e.strerror))
        sys.stderr.write('_ignore_signal({0:d}) failed: {1:d} ({2:s})\n'.format(signo, e.errno, e.strerror))
        sys.exit(1)
    logger.info('_ignore_signal({0:d}) exit'.format(signo))

__author__ = 'andrey.ushakov'
