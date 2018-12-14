# docker-ai_consul

This image is based on pieces of [official](https://github.com/hashicorp/docker-consul) `consul` image,
 BUT with several changes which fit ait infrastructure:

 * This image **runs on ubuntu:16**. official image runs on alpine, we would have problems on it, since most our health checks target ubuntu.
 * we don't use docker volume, but rely on bind mounts from host.
 * consul agent **runs as root**. Because we need it to be able to access a lot of external/out of container resources.
 If we had to coordinate uid/gid of consul in docker container with uid/gid of all other container, that would be a PITA (like on aga archive and backup).
 * we pack all our common checks and scripts into the image and reuse on all deployments. While official image is empty alpine.

## Usage

Most of the official consul image functionality is preserved, you should read [their intro](https://www.hashicorp.com/blog/official-consul-docker-image.html).
It comes down to following features:

 * run `docker run -ti --rm ai_consul:latest` to get a development/testing single node cluster,
 which has all data in memory, listens on `0.0.0.0` and has web UI.
 * usually you'll want to run with `--net=host`.
 * You can set `CONSUL_BIND_INTERFACE` to the name of the interface you'd like to
  bind to and this will look up the IP and pass the proper -bind= option along
  to Consul.
 * You can set `CONSUL_CLIENT_INTERFACE` to the name of the interface you'd like to
  bind client intefaces (HTTP, DNS, and RPC) to and this will look up the IP and
  pass the proper -client= option along to Consul.
 * `CONSUL_DATA_DIR=/consul/data` is exposed for possible persistent storage.
 * In the `CONSUL_CONFIG_DIR=/consul/config` you can compose additional config files if you use this image as a base.
 * You can also set the CONSUL_LOCAL_CONFIG environemnt variable to pass some
  Consul configuration JSON without having to bind any volumes.
  The content of variable will be saved to `$CONSUL_CONFIG_DIR/local.json` on container start.
 * in servers mount `/consul/data`.
 * in production run at least with `docker run ai_consul:latest agent <your arguments>` and `-v <host-path>:/consul/data` for servers.
 Entrypoint will append `-data-dir=/consul/data -config-dir=/consul/config` to your arguments.
 By default the CMD is for development mode: `agent -dev -client 0.0.0.0`, so you must at least provide `agent` for CMD.
 * in 99% of cases you do not need `:rw` to mounted volumes,
 because we just check disk space or presence of files, prefer to mount with `:ro` for safety.
 * to monitor containers mount `-v /var/run/docker.sock:/var/run/docker.sock:ro`

### Checks

This section documents included checks in this image.

Packages:
 * nagios-plugins-standard
 * libnagios-plugin-perl

Docs: https://www.monitoring-plugins.org/doc/man/check_http.html

#### Scripts

##### check_mem

```
Usage: check_mem [-w|--warning=<percent> ] [ -c|--critical=<percent> ]
```

##### is_container_running

```
Usage: is_container_running [container_name]
```

##### seconds_from_creation

```
Usage: seconds_from_creation [-w <secs>] [-c <secs>] -f <file>
  --help     Help. Display this message and quit.
  <secs>     File must be no more than this many seconds old (default: warn 240 secs, crit 600)
```

```
$ seconds_from_creation -f ./releaser
FILE_AGE OK: ./releaser is 223 seconds old (== 3 minutes == 0 hours)
$ echo $?
0
$ seconds_from_creation -f ./pipeline.gocd.yaml
FILE_AGE CRITICAL: ./pipeline.gocd.yaml is 1887160 seconds old (== 31452 minutes == 524 hours)
$ echo $?
2
```

##### check_gocd_agent.py

```
$ python3 check_gocd_agent.py --help
Usage: check_gocd_agent.py [OPTIONS]

Options:
  --go-server-url TEXT      URL to GoCD server
  --go-agent-resource TEXT
  --help                    Show this message and exit.
```

```
$ python3 check_gocd_agent.py --go-agent-resource=backup_production
Found agent: go-agent-backup-production
$ echo $?
0
$ python3 check_gocd_agent.py --go-agent-resource=backup_product
Did not find agent with backup_product resource
$ echo $?
2
```

#### Openstack checks

Each check can use file with authorization details, e.g.
```
check_nova-services --filename /consul/config/openstack_creds.ini
```
where `openstack_creds.ini` has following format:
```
[DEFAULT]
username=admin
password=*****
tenant_name=admin
auth_url=http://192.168.200.17:35357/v3
```


`check_nova-services`
```
python openstacknagios/nova/Services.py
NOVASERVICES OK - [up:5 disabled:0 down:0 total:5] | disabled=0;@1:;;0 down=0;;0;0 total=5;;@0;0 up=5;;;0
```

`check_nova-hypervisors`
```
python openstacknagios/nova/Hypervisors.py --warn_vcpus_percent 0:150 --critical_vcpus_percent 0:200
NOVAHYPERVISORS OK - [memory_used:28160 memory_percent:44 vcpus_used:21 vcpus_percent:131 running_vms:13] | memory_percent=44;90;95;0;100 memory_used=28160;;;0;63838 running_vms=13;;;0 vcpus_percent=131;150;200;0;100 vcpus_used=21;;;0;16
```

`check_neutron-agents`
```
python openstacknagios/neutron/Agents.py
NEUTRONAGENTS OK - [up:14 disabled:0 down:0] | disabled=0;@1:;;0 down=0;;0;0 total=14;;@0;0 up=14;;;0
```

`check_cinder-services`
```
python openstacknagios/cinder/Services.py
CINDERSERVICES OK - [up:4 disabled:0 down:0 total:4] | disabled=0;@1:;;0 down=0;;0;0 total=4;;@0;0 up=4;;;0
```

`check_glance-images`
```
python openstacknagios/glance/Images.py
GLANCEIMAGES OK - [gettime:0.0003068] | gettime=0.000306844711304;;;0
```

# Development

If you see a missing check script, you should add it.

Scripts should be generic, not reference a specific deployment. For example,
it is OK to add scripts for validating mongodb, zookeeper or whatever other type of server.
But the scripts should not contain `.ai-traders.com`, assume that some remote service is present, etc.
