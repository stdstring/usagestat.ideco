from __future__ import unicode_literals
from datetime import datetime
import os
import subprocess


class CertificateValidator(object):

    # spec: int -> CertificateValidator
    def __init__(self, expiration_days):
        self.expiration_days = expiration_days
        self._container_dir = os.path.dirname(__file__)

    # spec: str -> bool
    def is_valid(self, cert_filename):
        command = [os.path.join(self._container_dir, 'get_cert_enddate.sh'), cert_filename]
        result = subprocess.check_output(command).rstrip('\n')
        cert_enddate = datetime.strptime(result, '%Y-%m-%d')
        today = datetime.today()
        days_rest = (cert_enddate - today).days
        return days_rest > self.expiration_days

__author__ = 'andrey.ushakov'
