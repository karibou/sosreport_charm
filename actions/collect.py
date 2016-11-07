#!/usr/bin/python3

from __future__ import division
from charmhelpers.core.hookenv import action_get
from charmhelpers.core.hookenv import action_set
from charmhelpers.core.hookenv import action_fail
from charmhelpers.core.hookenv import DEBUG
from charmhelpers.core.hookenv import log as juju_log
import sys
import os
import re
import shutil
from subprocess import check_output


def has_enough_space(mydir, minfree):
    '''
    Verify if filesystem has more than minfree% or minfree[M|G] of free space
    available. Valid suffixes are %, M or G
    '''
    # Set default values
    megabyte = 1048576
    gigabyte = 1073741824

    min_suffix = minfree[-1:]
    if min_suffix not in ['%', 'M', 'G']:
        action_msg = 'minfree: Invalid suffix : %s' % min_suffix
        action_fail(action_msg)
        return False

    try:
        min_spc = int(minfree[:-1])
    except ValueError as Err:
        action_msg = 'minfree: Invalid value : %s' % minfree[:-1]
        action_fail(action_msg)
        return False

    dirstat = os.statvfs(mydir)

    if min_suffix == '%':
        pctfree = int(dirstat.f_bavail / dirstat.f_blocks * 100)
        if min_spc < pctfree:
            return False
    else:
        if min_suffix == 'G':
            multiplier = gigabyte
        else:
            multiplier = megabyte

        spc_avail = int(dirstat.f_bavail * dirstat.f_bsize / multiplier)
        if spc_avail < min_spc:
            return False

    return True


def collect_sosreport():

    command = ['sosreport']
    default_option = ['--batch']
    juju_home = '/home/ubuntu'
    minfree = '5%'

    params = action_get()

    if params:
        if 'minfree' in params.keys():
            minfree = params['minfree']

        if 'homedir' in params.keys():
            if not os.path.isdir(params['homedir']):
                action_set({'outcome': 'failure'})
                action_msg = 'homedir: Invalid path - %s' % params['homedir']
                action_fail(action_msg)
                return
            juju_home = params['homedir']

    if not has_enough_space(juju_home, minfree):
        action_set({'outcome': 'failure'})
        action_msg = 'Not enough space in %s (minfree: %s )' % (
                     juju_home, minfree)
        action_fail(action_msg)
        return

    try:
        juju_log("Running %s %s" % (command, default_option), level=DEBUG)
        sosrun = check_output(command + default_option,
                              universal_newlines=True)
        regex = re.compile(r' /tmp.*tar.*')
        tarball = regex.findall(sosrun)[0].lstrip(' ')
        md5sum = tarball + '.md5'
        juju_log("Moving %s in %s" % (tarball, juju_home), level=DEBUG)
        shutil.move(tarball, juju_home)
        juju_log("Moving %s in %s" % (md5sum, juju_home), level=DEBUG)
        shutil.move(md5sum, juju_home)
        action_msg = '%s and %s available in %s' % (tarball.lstrip('/tmp/'),
                                                    md5sum.lstrip('/tmp/'),
                                                    juju_home)
        action_set({'result-map.message': action_msg})
        action_set({'outcome': 'success'})
        return
    except Exception as Err:
        action_set({'outcome': 'failure'})
        action_msg = 'Unable to run sosreport'
        action_fail(action_msg)
        return


def main():
    collect_sosreport()

if __name__ == '__main__':
    main()
