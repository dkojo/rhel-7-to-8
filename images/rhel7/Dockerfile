# A RHEL 7.9 host as it was set up years ago, by hand: the orders portal on Python 2.7, with a systemd unit enabled at boot.
# RHEL 7's systemd (v219) can't run as PID 1 on today's cgroup v2 hosts, so in this container the portal itself is the
# main process. The unit file and its "enabled" link are still there, exactly as on the real servers.
FROM registry.access.redhat.com/ubi7/ubi:7.9
COPY app/portal.py /opt/portal/portal.py
RUN printf '[Unit]\nDescription=Orders portal\n\n[Service]\nExecStart=/usr/bin/python2 /opt/portal/portal.py\nRestart=always\n\n[Install]\nWantedBy=multi-user.target\n' \
      > /etc/systemd/system/portal.service \
 && mkdir -p /etc/systemd/system/multi-user.target.wants \
 && ln -s /etc/systemd/system/portal.service /etc/systemd/system/multi-user.target.wants/portal.service
CMD ["/usr/bin/python2", "/opt/portal/portal.py"]
