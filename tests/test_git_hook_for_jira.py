#!/usr/bin/env python
#
#  XXX  Identifying information about tests here.
#
#===============
#  This is based on a skeleton test file, more information at:
#
#     https://github.com/linsomniac/python-unittest-skeleton

import unittest

import os
import sys
sys.path.append('..')      # XXX Probably needed to import your code


class test_git_hook_for_jira(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_git_hook(self):

        raise NotImplementedError('Insert test code here.')
        #  Examples:
        # self.assertEqual(fp.readline(), 'This is a test')
        # self.assertFalse(os.path.exists('a'))
        # self.assertTrue(os.path.exists('a'))
        # self.assertTrue('already a backup server' in c.stderr)
        # self.assertIn('fun', 'disfunctional')
        # self.assertNotIn('crazy', 'disfunctional')
        # with self.assertRaises(Exception):
        #	raise Exception('test')
        #
        # Unconditionally fail, for example in a try block that should raise
        # self.fail('Exception was not raised')

    @unittest.skipIf('SKIP_SLOW_TESTS' in os.environ, 'Requested fast tests')
    def test_XXX_Slow_Test_Name(self):
        raise NotImplementedError('Insert test code here.')

unittest.main()