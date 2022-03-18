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

from pykmm.kmm.items import *

class TestKeyItem(unittest.TestCase):
    def setUp(self):
        """Test setup."""
        self._keyitem = KeyItem()

    def tearDown(self):
        """Tear down."""
        del self._keyitem

    def test_sln(self):
        """Test all SLN get, set, and invalid paths"""

        # set the SLN then get it
        self._keyitem.sln = 0x1234
        self.assertEqual(self._keyitem.sln, 0x1234)

        self._keyitem.sln = 156
        self.assertEqual(self._keyitem.sln, 156)

        #test with invalid types
        with self.assertRaises(TypeError):
            self._keyitem.sln = "beans"

        with self.assertRaises(TypeError):
            self._keyitem.sln = [0x0, 0x1, 0x2, 0x3]

        #test with invalid bounds
        with self.assertRaises(ValueError):
            self._keyitem.sln = -256

        with self.assertRaises(ValueError):
            self._keyitem.sln = 0xFFFFFF

    def test_kid(self):
        """Test all KID get, set, and invalid paths"""

        # set the kid then get it
        self._keyitem.kid = 0x1234
        self.assertEqual(self._keyitem.kid, 0x1234)

        self._keyitem.kid = 156
        self.assertEqual(self._keyitem.kid, 156)

        #test with invalid types
        with self.assertRaises(TypeError):
            self._keyitem.kid = "beans"

        with self.assertRaises(TypeError):
            self._keyitem.kid = [0x0, 0x1, 0x2, 0x3]

        #test with invalid bounds
        with self.assertRaises(ValueError):
            self._keyitem.kid = -256

        with self.assertRaises(ValueError):
            self._keyitem.kid = 0xFFFFFF

    def test_key(self):
        """Test all key get, set, and invalid paths"""

        # set the key then get it
        self._keyitem.key = 0x1234
        self.assertEqual(self._keyitem.key, 0x1234)

        self._keyitem.key = 156
        self.assertEqual(self._keyitem.key, 156)

        #test with AES key
        keyValue = 0x3773F47225F4497210358367DEDD55996AB8F774B41FD945888E2E1958DAA025
        self._keyitem.key = keyValue
        self.assertEqual(self._keyitem.key, keyValue)

        #test with DES-OFB key
        keyValue = 0xDCF8D675984A75F4
        self._keyitem.key = keyValue
        self.assertEqual(self._keyitem.key, keyValue)

        #test with ADP key
        keyValue = 0x71D4C373D6
        self._keyitem.key = keyValue
        self.assertEqual(self._keyitem.key, keyValue)

        #test with invalid types
        with self.assertRaises(TypeError):
            self._keyitem.key = "beans"

        with self.assertRaises(TypeError):
            self._keyitem.key = [0x0, 0x1, 0x2, 0x3]

    def test_key_tobytes(self):
        """Test turning the KeyItem object to bytes"""
        self._keyitem.key = 0x71D4C373D6
        self._keyitem.sln = 0x1234
        self._keyitem.kid = 0x5678
        self._keyitem.erase = False
        self._keyitem.kek = False

        resultBytes = self._keyitem.to_bytes()
        testBytes = b'\x00\x00'
        self.assertEqual(resultBytes, testBytes)

if __name__ == '__main__':
    unittest.main()