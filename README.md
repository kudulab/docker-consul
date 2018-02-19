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
```

# Development

If you see a missing check script, you should add it.

Scripts should be generic, not reference a specific deployment. For example,
it is OK to add scripts for validating mongodb, zookeeper or whatever other type of server.
But the scripts should not contain `.ai-traders.com`, assume that some remote service is present, etc.
