import amulet
import requests
import unittest


class TestSosreportCharm(unittest.TestCase):
    def __init__(self, series):
        super(TestSosreportCharm, self).__init__()
        self.series = series
        self.seconds = 900

    def run_test(self):
        self.deployment = amulet.Deployment(series=self.series)
        self.deployment.log.debug("Starting tests for %s" % self.series)
        self.deployment.add('sosreport')

        try:
            self.deployment.setup(timeout=self.seconds)
            self.deployment.sentry.wait(self.seconds)
            self.deployment.log.debug("starting deployment for %d seconds" %
                                      self.seconds)
        except amulet.helpers.TimeoutError:
            message = ('The environment did not setup in %d seconds.' %
                       self.seconds)
            # The SKIP status enables skip or
            # fail the test based on configuration.
            amulet.raise_status(amulet.SKIP, msg=message)
        except:
            raise

        self.unit = self.deployment.sentry['sosreport'][0]
        self.service_stat = self.unit.info['agent-state']
        self.file_stat = self.unit.file('/usr/bin/sosreport')
        self.deployment.log.debug("Testing if the service is started")
        self.assertEqual(self.service_stat, 'started')
        self.deployment.log.debug("Testing if the sosreport executable exists")
        self.assertEqual(self.file_stat['uid'], 0)
        self.assertEqual(self.file_stat['gid'], 0)
