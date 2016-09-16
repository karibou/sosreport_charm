import mock
import shutil
import tempfile

import unittest

import actions.collect as collect


class fake_statvfs():
    f_bavail = 0
    f_blocks = 0
    f_bsize = 0


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

        self.has_enough_space.return_value = False
        self.patch(collect, 'action_fail')
        collect.collect_sosreport()
        self.assertTrue(self.action_fail.call_args_list[0][0][0].startswith(
                        'Not enough space'))

    def test_collect_with_wrong_dir(self):
        self.patch(collect, 'action_get',
                   return_value={'homedir': '/wrongdir'})
        self.patch(collect, 'has_enough_space', return_value=True)
        self.patch(collect.os.path, 'isdir', return_value=False)
        self.patch(collect, 'action_fail')

        collect.collect_sosreport()
        self.action_fail.assert_called_with(
            'homedir: Invalid path - /wrongdir')

    def test_has_enough_space(self):
        onegig = 1073741824
        fake_dirstat = fake_statvfs()
        fake_dirstat.f_bavail = 5 * onegig
        fake_dirstat.f_blocks = 100 * onegig
        fake_dirstat.f_bsize = 1

        self.patch(collect.os, 'statvfs', return_value=fake_dirstat)

        ret = collect.has_enough_space('/fake', 5, 1)
        self.assertTrue(ret, '10 avail blocks should be higher than default')

        fake_dirstat.f_bavail = 2 * onegig
        ret = collect.has_enough_space('/fake', 5, 1)
        self.assertTrue(ret, '2 gig should be more than mingig')

        fake_dirstat.f_bavail = 0.5 * onegig
        ret = collect.has_enough_space('/fake', 5, 1)
        self.assertFalse(ret, '500M should be too small')
