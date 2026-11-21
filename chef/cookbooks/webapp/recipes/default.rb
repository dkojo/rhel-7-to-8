# Configures the orders portal on a RHEL 8 host. The Ansible rolling upgrade runs it in local mode:
#   cinc-client -z -o webapp
# RHEL 8 has no Python 2, so the portal runs on Python 3 here. Everything else matches the RHEL 7 hosts.

package 'python3'

directory '/opt/portal'

cookbook_file '/opt/portal/portal.py' do
  source 'portal.py'
  mode '0644'
  notifies :restart, 'service[portal]'
end

systemd_unit 'portal.service' do
  content <<~UNIT
    [Unit]
    Description=Orders portal

    [Service]
    ExecStart=/usr/bin/python3 /opt/portal/portal.py
    Restart=always

    [Install]
    WantedBy=multi-user.target
  UNIT
  action [:create, :enable]
  notifies :restart, 'service[portal]'
end

service 'portal' do
  action [:enable, :start]
end
