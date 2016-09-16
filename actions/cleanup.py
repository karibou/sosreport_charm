#!/usr/bin/python3

from charmhelpers.core.hookenv import action_get
from charmhelpers.core.hookenv import action_set
from charmhelpers.core.hookenv import action_fail
from charmhelpers.core.hookenv import DEBUG
from charmhelpers.core.hookenv import log as juju_log
import sys
import os



def do_cleanup():
    juju_home = '/home/ubuntu'
    params = action_get()

    if params:
        if 'homedir' in params.keys():
            if not os.path.isdir(params['homedir']):
                action_set({'outcome': 'failure'})
                action_msg = 'homedir: Invalid path - %s' % params['homedir']
                action_fail(action_msg)
                return
            juju_home = params['homedir']

    try:
        juju_log("Cleaning up %s" % juju_home, level=DEBUG)
        for (path, name, files) in os.walk(juju_home):
            for sosfile in files:
                if (os.path.exists(path + "/" + sosfile) and
                        sosfile.startswith('sosreport-')):
                    os.unlink(path + "/" + sosfile)
        action_msg = 'Directory %s cleaned up' % juju_home
        action_set({'result-map.message': action_msg})
        action_set({'outcome': 'success'})
        return
    except Exception as Err:
        action_set({'outcome': 'failure'})
        action_msg = 'Unable to cleanup %s' % juju_home
        action_fail(action_msg)
        return


def main():
    do_cleanup()

if __name__ == '__main__':
    main()
