# A RHEL 7.9 host as it was set up years ago, by hand: the orders portal on Python 2.7 as a systemd service.
FROM registry.access.redhat.com/ubi7/ubi-init:7.9
COPY app/portal.py /opt/portal/portal.py
RUN printf '[Unit]\nDescription=Orders portal\n\n[Service]\nExecStart=/usr/bin/python2 /opt/portal/portal.py\nRestart=always\n\n[Install]\nWantedBy=multi-user.target\n' \
      > /etc/systemd/system/portal.service \
 && systemctl enable portal
CMD ["/sbin/init"]
