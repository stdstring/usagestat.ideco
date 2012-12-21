from __future__ import unicode_literals
from stat_file_source.handler.transform_variable_handler import TransformVariableHandler
from stat_file_source.utils.standard_key_transformer import StandardKeyTransformer

KEY_VALUE_DELIMITER = '='

def _create_enable_variable_handler(variable_name):
    ENABLED = 'enabled'
    DISABLED = 'disabled'
    UNKNOWN = 'unknown'

    def transform_number(number_value):
        if number_value == 1:
            return ENABLED
        if number_value == 0:
            return DISABLED
        return UNKNOWN

    return TransformVariableHandler.create_with_known_key_list(KEY_VALUE_DELIMITER, [variable_name], StandardKeyTransformer, transform_number, DISABLED)

# TODO (std_string): think about some grouping in categories
handlers_def = [_create_enable_variable_handler('KAV4WEB_ENABLED'), # antivirus
                _create_enable_variable_handler('KAV4MAIL_ENABLED'), # antivirus
                _create_enable_variable_handler('CLAM4WEB_ENABLED'), # antivirus
                _create_enable_variable_handler('CLAM4MAIL_ENABLED'), # antivirus
                _create_enable_variable_handler('BA_ON'), # firewall
                _create_enable_variable_handler('DLP_WEB_ON'), # dlp
                _create_enable_variable_handler('DLP_MAIL_ON'), # dlp
                _create_enable_variable_handler('DLP_ICQ_ENABLED'), # dlp
                _create_enable_variable_handler('POSTFIX_ENABLED'), # mail
                _create_enable_variable_handler('POP3D_ENABLED'), # mail
                _create_enable_variable_handler('IMAPD_ENABLED'), # mail
                _create_enable_variable_handler('MAIL_FETCHMAIL'), # mail
                _create_enable_variable_handler('WEBMAIL_E_ENABLED'), #mail
                _create_enable_variable_handler('WEBMAIL_L_ENABLED'), # mail
                _create_enable_variable_handler('KSP4MAIL_ENABLED'), # antispam
                _create_enable_variable_handler('DSPAM_ENABLED'), # antispam
                _create_enable_variable_handler('THTTPD_E_ENABLED'), # web-server
                _create_enable_variable_handler('FTP_ENABLED'), # ftp-server
                _create_enable_variable_handler('JABBERD2_ENABLED'), # jabber-server
                _create_enable_variable_handler('PPTPD_ENABLED'), # pptp-server
                _create_enable_variable_handler('DHCPD_ENABLED'), # dhcp-server
                _create_enable_variable_handler('WINS_ENABLED'), # wins-server
                _create_enable_variable_handler('SNMPD_ENABLED'), # snmp-server
                _create_enable_variable_handler('BIND_ENABLED') # dns-server
                ]

__author__ = 'andrey.ushakov'
