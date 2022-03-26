#!/usr/bin/env python
#
# PyKMM - KMM and keyloading for Python
# GPLv2 Open Source. Use is subject to license terms.
# DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
#
# @package PyKMM
#
###############################################################################
#   Copyright (C) 2022 Natalie Moore <natalie@natnat.xyz>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
###############################################################################

import unittest

import pykmm.utility as utility

class TestUtility(unittest.TestCase):
    def setUp(self):
        """Test setup."""
        pass

    def tearDown(self):
        """Tear down."""
        pass

    def test_string_to_byte_list(self):
        """Test string to list"""
        self.assertEqual(utility.stringToByteList("C0FFEE"), [0xC0, 0xFF, 0xEE])

    def test_dataformat_int(self):
        '''Test all data format options for single int'''
        self.assertEqual(utility.dataFormat(0xff), "0xff")
        self.assertEqual(utility.dataFormat([0xc0, 0xff, 0xee]), "0xc0, 0xff, 0xee")
        self.assertEqual(utility.dataFormat(0xff), "0xff")
        self.assertEqual(utility.dataFormat(0xff), "0xff")
        self.assertEqual(utility.dataFormat(0), "0x00")

    def test_dataformat_list(self):
        '''Test all data format options for list'''

if __name__ == '__main__':
    unittest.main()