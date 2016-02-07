# -*- coding: utf-8 -*-
"""
Test Sage Package Handling
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
from sage_bootstrap.package import Package
from sage_bootstrap.expand_class import PackageClass



class TestPackageClass(unittest.TestCase):

    def test_expand_name(self):
        pc = PackageClass('pari')
        self.assertEqual(pc.names, ['pari'])

    def test_expand_all(self):
        pc = PackageClass(':all:')
        self.assertTrue(len(pc.names) > 10)

    def test_expand_standard(self):
        pc = PackageClass(':standard:')
        self.assertTrue(len(pc.names) > 10)

    def test_expand_optional(self):
        pc = PackageClass(':optional:')
        self.assertTrue(len(pc.names) > 10)

    def test_expand_experimental(self):
        pc = PackageClass(':experimental:')
        self.assertTrue(len(pc.names) > 2)

    def test_expand_huge(self):
        pc = PackageClass(':huge:')
        self.assertTrue(len(pc.names) >= 0)
        
    def test_apply(self):
        result = []
        def foo(arg1, arg2, kwd=None):
            result.append(arg1)
            self.assertEqual(arg2, 'second positional argument')
            self.assertEqual(kwd, 'keyword argument')
        pc = PackageClass(':all:')
        pc.apply(foo, 'second positional argument', kwd='keyword argument')
        self.assertEqual(result, pc.names)

            
