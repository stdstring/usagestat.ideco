Summary: Usage statistics subsystem
Name: usage_stat
Version: 1.0.b1
Release: 1
License: Ideco License
#Source: git@mastergit.ideco:/ics26/usagestat.git
Packager: Andrey Ushakov <a_ushakov@ideco.ru>

%description
usage_stat spec file 4 rpm

%build
python ../stat_sender_db/create.py ../stat_sender_db/usage_stat.db

%install
mkdir -p $RPM_BUILD_ROOT/var/lib/usage_stat/
mkdir -p $RPM_BUILD_ROOT/etc/cron.d/
cp ../stat_sender_db/usage_stat.db $RPM_BUILD_ROOT/var/lib/usage_stat/
cp ../prerequisites/usage_stat_crontab $RPM_BUILD_ROOT/etc/cron.d/
cp ../prerequisites/usage_stat_component_runner.sh $RPM_BUILD_ROOT/etc/cron.d/

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

# config ics.conf
if [ -z "grep "^USAGE_STAT_ENABLED" ]
then
  echo 'USAGE_STAT_ENABLED' >> /etc/ics/ics.conf
fi

%files
%attr(644, root, root) /etc/cron.d/usage_stat_crontab
%attr(555, root, root) /etc/cron.d/usage_stat_component_runner.sh
%attr(664, usage_stat, usage_stat) /var/lib/usage_stat/usage_stat.db