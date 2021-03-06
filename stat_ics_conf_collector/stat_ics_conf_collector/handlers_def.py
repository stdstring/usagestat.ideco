from __future__ import unicode_literals
import re
from stat_file_source.handler.aggregate_key_value_handler import AggregateKeyValueHandler
from stat_file_source.handler.transform_variable_handler import TransformVariableHandler

# common
KEY_VALUE_DELIMITER = '='
ENABLED = 'enabled'
DISABLED = 'disabled'
UNKNOWN = 'unknown'
# categories
KAV4Web = 'antivirus.KAV.WEB'
KAV4Mail = 'antivirus.KAV.MAIL'
Clam4Web = 'antivirus.ClamAV.WEB'
Clam4Mail = 'antivirus.ClamAV.MAIL'
Firewall = 'firewall.BA'
DLPWeb = 'dlp.WEB'
DLPMail = 'dlp.MAIL'
DLPIcq = 'dlp.ICQ'
Postfix = 'mail.POSTFIX'
POP3 = 'mail.POP3'
IMAP = 'mail.IMAP'
FetchMail = 'mail.FETCHMAIL'
ExternalWebMail = 'mail.WEBMAIL.External'
LocalWebMail = 'mail.WEBMAIL.Local'
KSP4Mail = 'antispam.KSP.MAIL'
DSpam = 'antispam.DSPAM'
WebServer = 'server.WEB'
FtpServer = 'server.FTP'
JabberServer = 'server.JABBER'
PPTPServer = 'server.PPTP'
DHCPServer = 'server.DHCP'
WinsServer = 'server.WINS'
SNMPServer = 'server.SNMP'
DNSServer = 'server.DNS'

def _create_net_type_count_handler():
    prepared_re = re.compile('^NET_IF\d+_TYPE$')
    known_key_predicate = lambda key, state: prepared_re.match(key) is not None
    key_transformer = lambda key, value, state: 'net_type.{0:s}'.format(value.strip("'"))
    aggregate_fun = lambda old_value, item: old_value + 1
    return AggregateKeyValueHandler(KEY_VALUE_DELIMITER, known_key_predicate, key_transformer, aggregate_fun, 0)

def _create_enable_variable_handler(variable_name, key_name):

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
                _create_enable_variable_handler('KAV4WEB_ENABLED', KAV4Web), # antivirus
                _create_enable_variable_handler('KAV4MAIL_ENABLED', KAV4Mail), # antivirus
                _create_enable_variable_handler('CLAM4WEB_ENABLED', Clam4Web), # antivirus
                _create_enable_variable_handler('CLAM4MAIL_ENABLED', Clam4Mail), # antivirus
                _create_enable_variable_handler('BA_ON', Firewall), # firewall
                _create_enable_variable_handler('DLP_WEB_ON', DLPWeb), # dlp
                _create_enable_variable_handler('DLP_MAIL_ON', DLPMail), # dlp
                _create_enable_variable_handler('DLP_ICQ_ENABLED', DLPIcq), # dlp
                _create_enable_variable_handler('POSTFIX_ENABLED', Postfix), # mail
                _create_enable_variable_handler('POP3D_ENABLED', POP3), # mail
                _create_enable_variable_handler('IMAPD_ENABLED', IMAP), # mail
                _create_enable_variable_handler('MAIL_FETCHMAIL', FetchMail), # mail
                _create_enable_variable_handler('WEBMAIL_E_ENABLED', ExternalWebMail), #mail
                _create_enable_variable_handler('WEBMAIL_L_ENABLED', LocalWebMail), # mail
                _create_enable_variable_handler('KSP4MAIL_ENABLED', KSP4Mail), # antispam
                _create_enable_variable_handler('DSPAM_ENABLED', DSpam), # antispam
                _create_enable_variable_handler('THTTPD_E_ENABLED', WebServer), # web-server
                _create_enable_variable_handler('FTP_ENABLED', FtpServer), # ftp-server
                _create_enable_variable_handler('JABBERD2_ENABLED', JabberServer), # jabber-server
                _create_enable_variable_handler('PPTPD_ENABLED', PPTPServer), # pptp-server
                _create_enable_variable_handler('DHCPD_ENABLED', DHCPServer), # dhcp-server
                _create_enable_variable_handler('WINS_ENABLED', WinsServer), # wins-server
                _create_enable_variable_handler('SNMPD_ENABLED', SNMPServer), # snmp-server
                _create_enable_variable_handler('BIND_ENABLED', DNSServer) # dns-server
                ]

initial_state_def = [(KAV4Web, DISABLED),
                     (KAV4Mail, DISABLED),
                     (Clam4Web, DISABLED),
                     (Clam4Mail, DISABLED),
                     (Firewall, DISABLED),
                     (DLPWeb, DISABLED),
                     (DLPMail, DISABLED),
                     (DLPIcq, DISABLED),
                     (Postfix, DISABLED),
                     (POP3, DISABLED),
                     (IMAP, DISABLED),
                     (FetchMail, DISABLED),
                     (ExternalWebMail, DISABLED),
                     (LocalWebMail, DISABLED),
                     (KSP4Mail, DISABLED),
                     (DSpam, DISABLED),
                     (WebServer, DISABLED),
                     (FtpServer, DISABLED),
                     (JabberServer, DISABLED),
                     (PPTPServer, DISABLED),
                     (DHCPServer, DISABLED),
                     (WinsServer, DISABLED),
                     (SNMPServer, DISABLED),
                     (DNSServer, DISABLED)]

__author__ = 'andrey.ushakov'
