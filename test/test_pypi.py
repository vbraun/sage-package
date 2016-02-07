# -*- coding: utf-8 -*-
"""
Test PyPi Interface
"""

#*****************************************************************************
#       Copyright (C) 2015 Volker Braun <vbraun.name@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************


import unittest

from sage_bootstrap.pypi import PyPiVersion, PyPiError, PyPiNotFound


class TestPyPiVersion(unittest.TestCase):

    def test_json_url(self):
        p = PyPiVersion('argparse')
        self.assertEqual(p.json_url, 'https://pypi.python.org/pypi/argparse/json')

    def test_json_download(self):
        p = PyPiVersion('argparse')
        self.assertTrue(p.json['info']['description'].startswith('The argparse module makes it easy'))

    def test_latest_version(self):
        p = PyPiVersion('argparse')
        self.assertTrue(isinstance(p.version, unicode))
        self.assertEqual(p.version, p.json['info']['version'])

    def test_download_url(self):
        p = PyPiVersion('argparse')
        self.assertTrue(isinstance(p.url, unicode))
        self.assertTrue(p.url.startswith('http'))
        self.assertTrue(p.url.endswith('.tar.gz'))
        
    def test_error_unknown(self):
        with self.assertRaises(PyPiNotFound):
            PyPiVersion('nonexistentpackagename')

        
