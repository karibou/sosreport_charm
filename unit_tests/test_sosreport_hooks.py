from mock import patch
import shutil
import tempfile

import unittest

import reactive.sosreport as sosreport


class TestSosreportHooks(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_install_sosreport(self):
        patch.object(sosreport, 'set_state')
        patch.object(sosreport, 'apt_install')
        sosreport.install_sosreport()
        sosreport.set_state.assert_called_with('sosreport.ready')
        sosreport.apt_install.assert_called_once_with(['sosreport'])

        patch.object(sosreport, 'add_source')
        sosreport.config.return_value = 'ppa:myppa'
        sosreport.install_sosreport()
        sosreport.add_source.assert_called_with('ppa:myppa')

    def test_cleanup_sosreport(self):
        patch.object(sosreport, 'apt_purge')
        patch.object(sosreport, 'status_set')
        sosreport.cleanup()
        sosreport.apt_purge.assert_called_once_with(['sosreport'])
        sosreport.status_set.assert_called_with('active', 'Sosreport purged')

    def _get_last_conf_line(self, config_file):
        with open(config_file, 'r') as conf_file:
            for line in conf_file:
                continue
        return(line)