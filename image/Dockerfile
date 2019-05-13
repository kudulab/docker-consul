FROM ubuntu:16.04

# Nano, curl is for humans administrating/experimenting.
# python is for scripting
RUN apt-get update &&\
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends\
  software-properties-common \
  tzdata gnupg wget curl ca-certificates cron nano git tar unzip sudo rsync apt-transport-https ssh-client net-tools iputils-ping \
  python3.5 &&\
  apt-get -y autoremove && apt-get -y autoclean && apt-get -y clean &&\
  rm -rf /tmp/* /var/tmp/* && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/Yelp/dumb-init/releases/download/v1.2.1/dumb-init_1.2.1_amd64.deb
RUN dpkg -i dumb-init_*.deb

# This is the release of Consul to pull in.
ENV CONSUL_VERSION=1.5.0

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
RUN /bin/bash -c "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -" &&\
  echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable" > /etc/apt/sources.list.d/docker.list &&\
  apt-get update &&\
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends\
   docker-ce-cli=5:18.09.5~3-0~ubuntu-xenial &&\
  rm -Rf /var/lib/docker/* &&\
  rm -rf /var/lib/apt/lists/* && rm -rf /tmp/* /var/tmp/*

RUN apt-get update &&\
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends\
  nagios-plugins-standard libnagios-plugin-perl &&\
  apt-get -y autoremove && apt-get -y autoclean && apt-get -y clean &&\
  rm -rf /tmp/* /var/tmp/* && rm -rf /var/lib/apt/lists/*

RUN git clone --branch 0.2.1 https://github.com/kudulab/ops-base.git /tmp/ops-base &&\
   cd /tmp/ops-base/setup &&\
   ./install.sh &&\
   cd / && rm -rf /tmp/ops-base

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

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

COPY scripts/* /usr/bin/

# By default you'll get an insecure single-node development server that stores
# everything in RAM, exposes a web UI and HTTP endpoints, and bootstraps itself.
# Don't use this configuration for production.
CMD ["agent", "-dev", "-enable-script-checks", "-client", "0.0.0.0"]
