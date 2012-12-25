from __future__ import unicode_literals
import re
from stat_file_source.handler.aggregate_key_value_handler import AggregateKeyValueHandler
from stat_file_source.handler.transform_variable_handler import TransformVariableHandler

KEY_VALUE_DELIMITER = '='

def _create_net_type_count_handler():
    prepared_re = re.compile('^NET_IF\d+_TYPE$')
    known_key_predicate = lambda key, state: prepared_re.match(key) is not None
    key_transformer = lambda key, value, state: 'net_type.{0:s}'.format(value.strip("'"))
    aggregate_fun = lambda old_value, item: old_value + 1
    return AggregateKeyValueHandler(KEY_VALUE_DELIMITER, known_key_predicate, key_transformer, aggregate_fun, 0)

def _create_enable_variable_handler(variable_name, key_name):
    ENABLED = 'enabled'
    DISABLED = 'disabled'
    UNKNOWN = 'unknown'

    def transform_number(number_value):
        number_value = number_value.strip("'")
        if number_value == '1':
            return ENABLED
        if number_value == '0' or number_value == '':
            return DISABLED
        return UNKNOWN

    key_transformer = lambda key, value, state: key_name
    return TransformVariableHandler.create_with_known_key_list(KEY_VALUE_DELIMITER, [variable_name], key_transformer, transform_number, DISABLED)

handlers_def = [_create_net_type_count_handler(),
                _create_enable_variable_handler('KAV4WEB_ENABLED', 'antivirus.KAV4WEB'), # antivirus
                _create_enable_variable_handler('KAV4MAIL_ENABLED', 'antivirus.KAV4MAIL'), # antivirus
                _create_enable_variable_handler('CLAM4WEB_ENABLED', 'antivirus.ClamAV4WEB'), # antivirus
                _create_enable_variable_handler('CLAM4MAIL_ENABLED', 'antivirus.ClamAV4MAIL'), # antivirus
                _create_enable_variable_handler('BA_ON', 'firewall.BA'), # firewall
                _create_enable_variable_handler('DLP_WEB_ON', 'dlp.WEB'), # dlp
                _create_enable_variable_handler('DLP_MAIL_ON', 'dlp.MAIL'), # dlp
                _create_enable_variable_handler('DLP_ICQ_ENABLED', 'dlp.ICQ'), # dlp
                _create_enable_variable_handler('POSTFIX_ENABLED', 'mail.POSTFIX'), # mail
                _create_enable_variable_handler('POP3D_ENABLED', 'mail.POP3'), # mail
                _create_enable_variable_handler('IMAPD_ENABLED', 'mail.IMAP'), # mail
                _create_enable_variable_handler('MAIL_FETCHMAIL', 'mail.FETCHMAIL'), # mail
                _create_enable_variable_handler('WEBMAIL_E_ENABLED', 'mail.WEBMAIL_External'), #mail
                _create_enable_variable_handler('WEBMAIL_L_ENABLED', 'mail.WEBMAIL_Local'), # mail
                _create_enable_variable_handler('KSP4MAIL_ENABLED', 'antispam.KSP4MAIL'), # antispam
                _create_enable_variable_handler('DSPAM_ENABLED', 'antispam.DSPAM'), # antispam
                _create_enable_variable_handler('THTTPD_E_ENABLED', 'server.WEB'), # web-server
                _create_enable_variable_handler('FTP_ENABLED', 'server.FTP'), # ftp-server
                _create_enable_variable_handler('JABBERD2_ENABLED', 'server.JABBER'), # jabber-server
                _create_enable_variable_handler('PPTPD_ENABLED', 'server.PPTP'), # pptp-server
                _create_enable_variable_handler('DHCPD_ENABLED', 'server.DHCP'), # dhcp-server
                _create_enable_variable_handler('WINS_ENABLED', 'server.WINS'), # wins-server
                _create_enable_variable_handler('SNMPD_ENABLED', 'server.SNMP'), # snmp-server
                _create_enable_variable_handler('BIND_ENABLED', 'server.DNS') # dns-server
                ]

__author__ = 'andrey.ushakov'
