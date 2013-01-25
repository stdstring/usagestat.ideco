from __future__ import unicode_literals
import os
import shutil

DATA_DEST_DIR = '/tmp/usagestat_test/data/'
CODE_DEST_DIR = '/tmp/usagestat_test/code/'

class TestManager(object):

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

def copy_file_over(source, dest):
    if os.path.exists(dest):
        os.unlink(dest)
    shutil.copy2(source, dest)

def copy_dirtree_over(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(source, dest)

__author__ = 'andrey.ushakov'
