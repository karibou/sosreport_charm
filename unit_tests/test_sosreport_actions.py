import mock
import shutil
import tempfile

import unittest

import actions.collect as collect

class TestSosreportActions(unittest.TestCase):
    def setUp(self):
        super(TestSosreportActions, self).setUp()
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def patch(self, obj, attr, return_value=None):
        mocked = mock.patch.object(obj, attr)
        started = mocked.start()
        started.return_value = return_value
        setattr(self, attr, started)
        self.addCleanup(mocked.stop)

    def test_collect_with_defaults(self):
        self.patch(collect.shutil, 'move')
        self.patch(collect, 'has_enough_space', return_value=True)
        sosrun = '''
        line-1
        line-2
        line-3
         /tmp/sosreport-me.tar.xz
        last line
        '''
        self.patch(collect, 'check_output', return_value=sosrun)

        collect.collect_sosreport()
        self.assertEqual(self.move.call_count, 2)
        for move_arg in self.move.call_args_list:
            if move_arg[0] == '':
                pass
            self.assertEqual(move_arg[0][0].rstrip('.md5'),
                             '/tmp/sosreport-me.tar.xz',
                             'Invalid file moved')

        default_sos_call = (['sosreport', '--batch'],)
        self.assertTupleEqual(self.check_output.call_args_list[0][0],
                              default_sos_call, 'Invalid default options')
