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
