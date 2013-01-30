from __future__ import unicode_literals
import os
from stat_sender.certificate_manager.certificate_generator import CertificateGenerator
from stat_sender.certificate_manager.certificate_validator import CertificateValidator

class CertificateManager(object):

    def __init__(self, cert_dest_dir, cert_name, lifetime_days, expiration_days):
        self._key_filename = os.path.join(cert_dest_dir, cert_name + '.key')
        self._cert_request_filename = os.path.join(cert_dest_dir, cert_name + '.csr')
        self._cert_filename = os.path.join(cert_dest_dir, cert_name + '.crt')
        self._generator = CertificateGenerator(self._key_filename, self._cert_request_filename, self._cert_filename, lifetime_days)
        self._validator = CertificateValidator(expiration_days)

    # None -> (str, str)
    def get_cert_with_private_key(self):
        if os.path.exists(self._key_filename) and os.path.exists(self._cert_filename):
            if self._validator.is_valid(self._cert_filename):
                return (self._key_filename, self._cert_filename)
        self._clear()
        self._generator.generate()
        return (self._key_filename, self._cert_filename)


    def _clear(self):
        rm_file_if_exist(self._key_filename)
        rm_file_if_exist(self._cert_request_filename)
        rm_file_if_exist(self._cert_filename)

def rm_file_if_exist(filename):
    if os.path.exists(filename):
        os.unlink(filename)

__author__ = 'andrey.ushakov'
