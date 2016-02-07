# -*- coding: utf-8 -*-
"""
Test fileserver.sagemath.org interface
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
import tempfile

from sage_bootstrap.package import Package
from sage_bootstrap.fileserver import FileServer


class TestFileServer(unittest.TestCase):

    def test_package_directory(self):
        pkg = Package('configure')
        fs = FileServer()
        self.assertEqual(fs.upstream_directory(pkg), '/data/files/spkg/upstream/configure')
        
