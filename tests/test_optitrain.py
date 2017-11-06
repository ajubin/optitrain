# -*- coding: utf-8 -*-
"""
    Opittrai Tests
    ~~~~~~~~~~~~

    Tests the optitrain application.

    :copyright: (c) 2017 by Antoine Jubin.
    :license: BSD, see LICENSE for more details.
"""

import os
import tempfile
import pytest
import unittest
import optitrain

class OptitrainTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, optitrain.app.config['DATABASE'] = tempfile.mkstemp()
        optitrain.app.testing = True
        self.app = optitrain.app.test_client()
        with optitrain.app.app_context():
            optitrain.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(optitrain.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No trips here so far' in rv.data

if __name__ == '__main__':
    unittest.main()
