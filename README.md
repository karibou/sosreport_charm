Overview
--------

This is a "source" charm, which is intended to be strictly the top layer of a built charm.

Peparation
----------

To build this charm, issue the following command from the top charm directory :

 $ charm -v build

Usage
-----

This charm is meant to be deployed concurrently with an existing unit from whic
we want to gather sosreport data. A typical syntax to deploy to a unit running
on machine #1 would be :

 $ juju deploy sosreport_charm --to=1

The charm will deploy to this machine and install sosreport. No actual data will
be collected. Sosreport installation will default to the version available in
the official Ubuntu archive. This can be changed by using the repository parameter.

Optional parameter
------------------

The sosreport_charm has one optional paramter :

 * repository : Any valid repository URL as understood by the add-apt-repository
		such as :
		ppa:canonical-support/support-tools
		deb http://archive.ubuntu.com/ubuntu/ trusty main

Actions
-------

This charm defines two actions :
 * collect : Action responsible for running sosreport and creating the report
 * cleanup : Action responsible for deleting all previously created reports

Action's parameters
-------------------

The collect action has the following optional parameters :
 * options : Valid options to be passed unchanged to sosreport
 * homedir : Alternate directory where reports will be stored. The directory
	     must exist (default: /home/ubuntu)
 * minfree : Minimum free space available to allow for a report to be created
	     (expressed in percent, default: 5)
 * mingig :  Minimum number of Gigabytes available to allow for a report to be
	     created (expressed in Gb, default: 1)

The cleanup action has the following optional parameter :
 * homedir : Alternate directory where stored reports needs to be deleted. The
	     directory (default: /home/ubuntu)
