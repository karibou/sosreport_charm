from charmhelpers.core.hookenv import status_set
from charmhelpers.core.hookenv import config
from charmhelpers.fetch import apt_install
from charmhelpers.fetch import apt_update
from charmhelpers.fetch import apt_purge
from charmhelpers.fetch import add_source
from charms.reactive import when_not, set_state, hook
from charmhelpers.core.hookenv import log as juju_log
from charmhelpers.core.hookenv import DEBUG

packages = ['sosreport']


@when_not('sosreport.installed')
def install_sosreport():
    '''Install sosreport'''
    # Do your setup here.
    #
    # If your charm has other dependencies before it can install,
    # add those as @when() clauses above., or as additional @when()
    # decorated handlers below
    #
    # See the following for information about reactive charms:
    #
    #  * https://jujucharms.com/docs/devel/developer-getting-started
    #  * https://github.com/juju-solutions/layer-basic#overview
    #
    status_set('maintenance', 'Installing sosreport')
    repo = config('repository')
    if repo != 'apt':
        add_source(repo)

    apt_update()
    apt_install(packages)

    set_state('sosreport.installed')
    status_set('active', 'sosreport is installed')

    set_state('sosreport.ready')


@hook('stop')
def cleanup():
    status_set('maintenance', 'Purging sosreport')
    apt_purge(packages)
    status_set('active', 'Sosreport purged')


@hook('config-changed')
def config_changed():
    repo = config('repository')
    if repo != 'apt':
        status_set('maintenance', 'Changing sosreport repository')
        juju_log("Changing sosreport repository to : %s" % repo, level=DEBUG)
        add_source(repo)
        apt_update()
        apt_install(packages)
        status_set('active', 'Sosreport repository updated')
