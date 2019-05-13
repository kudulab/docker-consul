# kudulab/consul docker image

This image is based on pieces of [official](https://github.com/hashicorp/docker-consul) `consul` image,
 BUT with several changes which fit kudulab infrastructure:

 * This image **runs on ubuntu:16**. official image runs on alpine, we would have problems on it, since most our health checks target ubuntu.
 * we don't use docker volume, but rely on bind mounts from host.
 * consul agent **runs as root**. Because we need it to be able to access a lot of external/out of container resources.
 If we had to coordinate uid/gid of consul in docker container with uid/gid of all other container, that would be a PITA.
 * we pack all our common checks and scripts into the image and reuse on all deployments. While official image is an empty alpine.

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

```
check_mem -w 80 -c 90
MEMORY CRITICAL - 94% used | used=31490465792B;26547391692.8;29865815654.4;0;33184239616 cached=1107591168B;;;0;33184239616 buffers=355876864B;;;0;33184239616 free=230305792B;;;0;33184239616
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
$ seconds_from_creation -f ./myfile
FILE_AGE OK: ./myfile is 223 seconds old (== 3 minutes == 0 hours)
$ echo $?
0
$ seconds_from_creation -f ./myfile
FILE_AGE CRITICAL: ./myfile is 1887160 seconds old (== 31452 minutes == 524 hours)
$ echo $?
2
```

##### check_gocd_agent.py

Checks if GoCD has a healthy agent with a specified resource.

```console
$ python3 check_gocd_agent.py --help
Usage: check_gocd_agent.py [OPTIONS]

Options:
  --go-server-url TEXT      URL to GoCD server
  --go-agent-resource TEXT
  --username TEXT
  --password-file TEXT
  --help                    Show this message and exit.
```

# Development

If you see a missing check script, you should add it.

Scripts should be generic, not reference a specific deployment. For example,
it is OK to add scripts for validating mongodb, zookeeper or whatever other type of server.
But the scripts should not contain any domains or assume that some remote service is present, etc.

## License

Copyright 2019 Ewa Czechowska, Tomasz Sętkowski

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
