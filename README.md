# PT-helper
tools for PT
need EditThisCookie


cp script/ubuntu/pthelper /etc/init.d
ln -s /etc/init.d/pthelper /etc/rc3.d/S99pthelper
update-rc.d pthelper defaults
systemctl daemon-reload