from __future__ import unicode_literals
import os
import subprocess

class CertificateGenerator(object):

    # spec: str, str, str, int -> CertificateGenerator
    def __init__(self, key_filename, cert_request_filename, cert_filename, lifetime_days):
        self._lifetime_days = lifetime_days
        self._key_filename = key_filename
        self._cert_request_filename = cert_request_filename
        self._cert_filename = cert_filename
        self._container_dir = os.path.dirname(__file__)

    # spec: None -> None
    def generate(self):
        self._generate_key()
        self._generate_cert_request()
        self._generate_cert()

    # spec: None -> None
    def _generate_key(self):
        gen_key_command = [os.path.join(self._container_dir, 'gen_key.sh'), self._key_filename]
        self._execute_interactive_command(gen_key_command, '')

    # spec: None -> None
    def _generate_cert_request(self):
        gen_cert_request_command = [os.path.join(self._container_dir, 'gen_cert_request.sh'), self._key_filename, self._cert_request_filename]
        # country name, state (province) name, locality name, organization name, organizational unit name, common name, email address, challenge password, optional company name
        input_list = ['RU', 'unknown state', 'unknown city', 'ideco client', 'unknown unit', 'ideco client', 'XXX@ideco.ru', 'ideco', 'ideco client']
        input = '\n'.join(input_list) + '\n'
        self._execute_interactive_command(gen_cert_request_command, input)

    # spec: None -> None
    def _generate_cert(self):
        gen_cert_command = [os.path.join(self._container_dir, 'gen_cert.sh'), self._key_filename, self._cert_request_filename, self._cert_filename, str(self._lifetime_days)]
        self._execute_interactive_command(gen_cert_command, '')

    # spec: str, str -> int
    def _execute_interactive_command(self, command, input):
        metascript_process = subprocess.Popen(args=command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if input != '':
            metascript_process.communicate(input)
        metascript_process.wait()
        return metascript_process.returncode

__author__ = 'andrey.ushakov'
