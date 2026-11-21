# A clean RHEL 8.10 host with Cinc (the free build of Chef Infra Client) and nothing else:
# the Chef recipe in chef/cookbooks/webapp does all the configuration, the same way on every host.
FROM registry.access.redhat.com/ubi8/ubi-init:8.10
RUN curl -fsSL https://omnitruck.cinc.sh/install.sh | bash -s -- -v 18 \
 && dnf clean all
CMD ["/sbin/init"]
