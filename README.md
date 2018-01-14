# Unix User Mangement with Consul Template

This is heavily based on CAULT (https://github.com/tolitius/cault)

A proof of concept of using [Consul](https://www.consul.io/) with [Consul-Template](https://github.com/hashicorp/consul-template/)  to build unix `passwd` and `group` files.  This has a few tools that mimic `useradd` and `groupadd`.  That when an etry is updated all machines running `consul-template`  will automatically rebuild their files.  No pushing files, no long lags.

## Why Do This?

In large clusters like those at [ARC-TS](http://arc-ts.umich.edu/) with over 1000 nodes, and users added/removed daily this might be faster than options based on `pdcp`.  As listed multiple services (clusters) can be defined.  Thus haivng users have uniqe data per cluster with only name and UID being constant.

## Why not LDAP?

This is more for those who have not worked on HPC clusters before.  We kill LDAP fast.  On a 1024 core parallel job using MPI-IO to read one file will DDOS most LDAP implimentations.  Using static files on the hosts proves more reliable and performant.

# Setting Up

* Build needed image: `docker-compose build`
* Pull images: `docker-compose pull`
* Start everything: `docker-compose up`
* Shell into the client container: `docker-compose exec client /bin/bash`
* Consul UI is running on `localhost:8500`

## adding users on client

```
cd /mnt/data

# add single user
./useradd.py --help
./useradd.py -a brockp --service flux -u 12345 -g 54321 -c "brock palen" -s "/bin/bash"
```

## Bulk Import passwd

```
cd /mnt/data

./importpasswd.py  -s flux -f passwd 
```

# Templates to generate passwd

* Download (consul-template)[https://releases.hashicorp.com/consul-template/]
* This is standalone go binary, and does not need to be ran in the client container
* Invoke on one of the tempaltes in `templates`
* `consul-template -template passwd-flux.ctpl -dry`
* To actually generate `/etc/passwd`
* `consul-template -template passwd-flux.ctpl:/etc/passwd`

# Shutdown

* `docker-compose down`

# TODO

* add group support and template
* add error checking 
* add UID filter
* add creating $HOME from `/etc/skel` like normal useradd
* Figureout how header for system users could be stand along file imported into template
