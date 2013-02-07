Summary: Usage statistics subsystem
Name: usage_stat
Version: 1.0.b1
Release: 1
Source: git@mastergit.ideco:/ics26/usagestat.git
Packager: Andrey Ushakov <a_ushakov@ideco.ru>

%build
python stat_sender_db/create.py stat_sender_db/usage_stat.db

%post
# create group and user
groupadd -g 13000 usage_stat
useradd -g 13000 -u 13000 -M -s /sbin/nologin usage_stat

# copy usage_stat.db
if [ ! -d "/var/lib/usage_stat/" ]
then
  mkdir /var/lib/usage_stat/
fi
cp stat_sender_db/usage_stat.db /var/lib/usage_stat/usage_stat.db

# config pam
if [ -z "grep '^\+ : usage_stat : cron crond$' /etc/security/access.conf" ] then
  echo '+ : usage_stat : cron crond' >> /etc/security/access.conf
fi

# config crontab
cp prerequisites/usage_stat_crontab /etc/cron.d/usage_stat_crontab
cp prerequisites/usage_stat_component_runner.sh /etc/cron.d/usage_stat_component_runner.sh

# config ics.conf
if [ -z "grep "^USAGE_STAT_ENABLED" ]
then
  echo 'USAGE_STAT_ENABLED' >> /etc/ics/ics.conf
fi

%files
stat_sender_db/usage_stat.db