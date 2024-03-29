### 1.0.0 (2019-May-13)

 * improved `check_gocd_agent.py` to support auth credentials
 * added consul 1.5.0
 * remove ai proxy usage
 * remove openstack checks, ceph
 * use new workflow scripts
 * use only python 3.5
 * added license

### 0.5.2 (2018-Dec-14)

* add check: `check_gocd_agent.py` #17043
* edit check: `seconds_from_creation` to show backup date also in minutes and
 hours #17014
* fix warnings from check: `check_mem` #17017, just use the fixed version from [github](https://github.com/jasonhancock/nagios-memory/blob/5c7b5620f74d6c2c280f378705883bc063a0f032/plugins/check_mem)

### 0.5.1 (2018-Dec-14)

 * remove signature check on consul which was failing gpg download
 * use locked dependencies when installing openstack checks

### 0.5.0 (2018-Jun-13)

 * added ubuntu-toolchain-r to support new ceph 13.2 and its newer libstdc++
 * added python2.7 and setup tools to support openstack checks
 * added openstack checks

### 0.4.0 (2018-Jun-11)

 * switch to python3.5
 * added ceph-common

### 0.3.0 (2018-May-23)

 * revert blitznote/debase as base image
 * update to consul 1.10 to try new UI

### 0.2.0 (2018-Apr-12)

 - use blitznote/debase as base image
 - drop python which is not used by any check
 - drop rake, which is not used, neither is ruby

### 0.1.0 (2018-Feb-28)

Initial release
