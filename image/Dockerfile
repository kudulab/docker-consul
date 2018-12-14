FROM ubuntu:16.04

COPY apt_cache /etc/apt/apt.conf.d/01_proxy

# Nano, curl is for humans administrating/experimenting.
# python is for scripting
RUN apt-get update &&\
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends\
  software-properties-common \
  tzdata gnupg wget curl ca-certificates cron nano git rake tar unzip sudo rsync apt-transport-https ssh-client net-tools iputils-ping \
  python-setuptools python3.5 &&\
  apt-get -y autoremove && apt-get -y autoclean && apt-get -y clean &&\
  rm -rf /tmp/* /var/tmp/* && rm -rf /var/lib/apt/lists/*

RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN /bin/bash -c "curl -fsSL http://apt.ai-traders.com/pubkey.gpg | sudo apt-key add -" &&\
  echo "deb [arch=amd64] http://apt.ai-traders.com/ceph/ Debian main" > /etc/apt/sources.list.d/ceph.list &&\
  apt-get update &&\
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends\
  ceph-common &&\
  rm -rf /var/lib/apt/lists/* && rm -rf /tmp/* /var/tmp/*

RUN wget https://github.com/Yelp/dumb-init/releases/download/v1.2.1/dumb-init_1.2.1_amd64.deb
RUN dpkg -i dumb-init_*.deb

# This is the release of Consul to pull in.
ENV CONSUL_VERSION=1.1.0

# This is the location of the releases.
ENV HASHICORP_RELEASES=https://releases.hashicorp.com

# Set up Consul.
RUN mkdir -p /tmp/build && \
    cd /tmp/build && \
    wget ${HASHICORP_RELEASES}/consul/${CONSUL_VERSION}/consul_${CONSUL_VERSION}_linux_amd64.zip && \
    wget ${HASHICORP_RELEASES}/consul/${CONSUL_VERSION}/consul_${CONSUL_VERSION}_SHA256SUMS && \
    grep consul_${CONSUL_VERSION}_linux_amd64.zip consul_${CONSUL_VERSION}_SHA256SUMS | sha256sum -c && \
    unzip -d /bin consul_${CONSUL_VERSION}_linux_amd64.zip && \
    cd /tmp && \
    rm -rf /tmp/build

RUN mkdir -p /consul/data /consul/config

# Install docker because checks use docker CLI
RUN /bin/bash -c "curl -fsSL http://apt-docker.ai-traders.com/pubkey.gpg | sudo apt-key add -" &&\
  echo "deb [arch=amd64] http://apt-docker.ai-traders.com/docker-new/ubuntu-xenial ubuntu-xenial edge" > /etc/apt/sources.list.d/docker.list &&\
  apt-get update &&\
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends\
  docker-ce=18.04.0~ce~3-0~ubuntu &&\
  rm -Rf /var/lib/docker/* &&\
  rm -rf /var/lib/apt/lists/* && rm -rf /tmp/* /var/tmp/*

RUN apt-get update &&\
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends\
  nagios-plugins-standard libnagios-plugin-perl &&\
  apt-get -y autoremove && apt-get -y autoclean && apt-get -y clean &&\
  rm -rf /tmp/* /var/tmp/* && rm -rf /var/lib/apt/lists/*

# openstack checks
RUN apt-get update &&\
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends\
  build-essential python-dev libffi-dev libssl-dev &&\
  apt-get -y autoremove && apt-get -y autoclean && apt-get -y clean &&\
  rm -rf /tmp/* /var/tmp/* && rm -rf /var/lib/apt/lists/*
RUN easy_install git+https://github.com/ai-traders/openstack-nagios-plugins.git

RUN git clone --branch 0.1.0 http://git.ai-traders.com/platform/python-ops.git /python-ops &&\
   cd /python-ops &&\
   ./install.sh &&\
   cd / && rm -rf /python-ops

# Server RPC is used for communication between Consul clients and servers for internal
# request forwarding.
EXPOSE 8300

# Serf LAN and WAN (WAN is used only by Consul servers) are used for gossip between
# Consul agents. LAN is within the datacenter and WAN is between just the Consul
# servers in all datacenters.
EXPOSE 8301 8301/udp 8302 8302/udp

# HTTP and DNS (both TCP and UDP) are the primary interfaces that applications
# use to interact with Consul.
EXPOSE 8500 8600 8600/udp

# Consul doesn't need root privileges so we run it as the consul user from the
# entry point script. The entry point script also uses dumb-init as the top-level
# process to reap any zombie processes created by Consul sub-processes.
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

COPY scripts/* /usr/bin/

# By default you'll get an insecure single-node development server that stores
# everything in RAM, exposes a web UI and HTTP endpoints, and bootstraps itself.
# Don't use this configuration for production.
CMD ["agent", "-dev", "-enable-script-checks", "-client", "0.0.0.0"]

ARG this_image_tag_arg
ARG this_image_name_arg
ENV this_image_tag=${this_image_tag_arg} this_image_name=${this_image_name_arg}
